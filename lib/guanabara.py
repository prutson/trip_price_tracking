from playwright.async_api import async_playwright

async def buscar_passagens_onibus(origem, destino, data, passageiros):
    url = f"https://viajeguanabara.com.br/onibus/{origem}/{destino}?departureDate={data}&passengers=1:{passageiros}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = await context.new_page()
        await page.goto(url)



        try:
            await page.wait_for_selector('.modal-wheel', state='detached', timeout=30000)
            await page.wait_for_timeout(5000)

            precos = await page.query_selector_all('[data-testid="tripPriceOutput"].value')
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
            print("Erro ao buscar preços:", e)
            return []
