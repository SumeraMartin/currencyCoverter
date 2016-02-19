# Currency converter

Aplikácia používa python s verziou 3.4

Aplikácia na svoj beh využíva služby [Finance Yahoo], pre túto stránku som sa rozhodol kvôli tomu že má pristupné služby ako zmenu menného kurzu a veľký počet mien a zdarma do 2000 requestov za deň, čo je pre nás dostačujúce.

Aplikácia využíva jednoduchý cache systém za pomoci súborov v ".cache" sdresáry. Databázu som sa rozhodol nepoužiť, lebo nevyužívam zložité dopyty a práca so súborom je nenáročná.

Cachujem dve veci: 

>Meny, ktoré sú získané zo stránky [all currencies] kde by maly byť všetky dôležité meny s ktorými finance yahoo pracuje. Cache je nastavená na 24 hodín, keďže tieto dáta by sa meniť nemali

>Premenné kurzy, ktoré získavám dopytom na [Finance Yahoo] a ktoré majú nastavenú cache na 5 minút.

Na premenu symbolu na kód meny využívam viacero zdrojov zozbieraných z internetu a spracovaných na jednoduchý súbor v súborw data/currencies_symbols.data.

# Návod
#### Základné pužitie
```sh
$./currency_converter.py --amount 10.0  --input_currency USD --output_currency EUR
```
#### Bez použitia cache, prepínač --noCache
```sh
$./currency_converter.py --amount 10.0  --input_currency USD --output_currency EUR --noCache
```
#### Zobraziť diagnostické dáta
```sh
$./currency_converter.py --amount 10.0  --input_currency USD --output_currency EUR --diagnostic
``` 
Výstup
```json
{
    "diagnostic": {
        "cachedData": true,
        "executionTime": 0.0005388259887695312
    },
    "input": {
        "amount": 10.0,
        "currency": "USD"
    },
    "output": {
        "EUR": 9.01
    }
}
```

# Testy
Jednoduché testy sa dajú spustiť s 
```sh
$./tests.py
```

[Finance Yahoo]: <https://finance.yahoo.com>
[all currencies]: <http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json>


