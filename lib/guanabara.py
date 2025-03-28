from playwright.async_api import async_playwright
from lib.shared import *
import traceback

async def buscar_passagens_onibus(origem, destino, data, passageiros):
    url = f"https://viajeguanabara.com.br/onibus/{origem}/{destino}?departureDate={data}&passengers=1:{passageiros}"
    log_message(f"Fazendo busca em: {url}")
    async with async_playwright() as p:
        # browser = await p.chromium.launch(
        #     headless=True,
        #     args=[
        #         "--no-sandbox",
        #         "--disable-setuid-sandbox",
        #         "--disable-dev-shm-usage",
        #         "--disable-blink-features=AutomationControlled"
        #     ]
        # )
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--proxy-server='direct://'",  # Ignora proxies
                "--proxy-bypass-list=*"         # 
            ]
        )
            
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True,
            bypass_csp=True
        )

        page = await context.new_page()
        await page.goto(url)

        try:
            await page.wait_for_selector('.modal-wheel', state='detached', timeout=30000)
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')  # Força renderização
            await page.wait_for_function(
                '''() => document.querySelectorAll('[data-testid="tripPriceOutput"]').length > 0''',
                timeout=60000
)

            precos = await page.query_selector_all('[data-testid="tripPriceOutput"].value')
            saidas = await page.query_selector_all('span.trip-time-number:nth-child(1)')
            chegadas = await page.query_selector_all('span.trip-time-number:nth-child(2)')
            categorias = await page.query_selector_all('[data-testid="tripClassNameOutput"]')

            log_message(f"precos: {precos}")
            log_message(f"saidas: {saidas}")
            log_message(f"chegadas: {chegadas}")
            log_message(f"categorias: {categorias}")

            resultados = []
            for i in range(min(len(precos), len(saidas), len(chegadas), len(categorias))):
                preco = await precos[i].inner_text()
                preco = preco.replace('\xa0', ' ').strip()
                saida = await saidas[i].inner_text()
                chegada = await chegadas[i].inner_text()
                categoria = await categorias[i].inner_text()

                resultados.append({
                    "DATA": data,
                    "ORIGEM": origem.upper(),
                    "DESTINO": destino.upper(),
                    "PASSAGEIROS": passageiros,
                    "SAIDA": saida,
                    "CHEGADA": chegada,
                    "CATEGORIA": categoria.strip(),
                    "PRECO": preco,
                })

            return resultados

        # except Exception as e:
        #     log_message(f"Erro ao buscar preços: {e}")
        #     return ["Erro ao buscar preços"]
        except Exception as e:
            log_message(f"Erro crítico: {str(e)}")
            log_message(f"Stack trace: {traceback.format_exc()}")  # Adicione esta linha
            return ["Erro ao buscar preços"]