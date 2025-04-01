from playwright.async_api import async_playwright
from lib.shared import *
import traceback

async def buscar_passagens_onibus(origem, destino, data, passageiros):
    url = f"https://viajeguanabara.com.br/onibus/{origem}/{destino}?departureDate={data}&passengers=1:{passageiros}"
    log_message(f"Fazendo busca em: {url}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )
            
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            java_script_enabled=True,
            bypass_csp=True
        )

        page = await context.new_page()
        # await page.goto(url)
        await page.goto(url, timeout=60000)


        try:
            await page.wait_for_selector('.modal-wheel', state='detached', timeout=45000)
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)') 
            await page.wait_for_function(
                '''() => document.querySelectorAll('[data-testid="tripPriceOutput"]').length > 0''',
                timeout=30000
            )

            precos = await page.query_selector_all('[data-testid="tripPriceOutput"]')
            saidas = await page.query_selector_all('span.trip-time-number:nth-child(1)')
            chegadas = await page.query_selector_all('span.trip-time-number:nth-child(2)')
            categorias = await page.query_selector_all('[data-testid="tripClassNameOutput"]')

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

        except Exception as e:
            log_message(f"Erro crítico: {str(e)}")
            log_message(f"Stack trace: {traceback.format_exc()}") 
            return ["Erro ao buscar preços"]