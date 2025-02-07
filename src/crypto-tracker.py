# encoding: utf-8

import sys
from workflow import Workflow, ICON_WEB, ICON_ERROR, web


def format_strings_from_quote(ticker, quote_data):
    data = quote_data['RAW'][ticker.upper()]['USD']
    price = '{:,.4f}'.format(data['PRICE'])
    high = '{:,.4f}'.format(data['HIGH24HOUR'])
    low = '{:,.4f}'.format(data['LOW24HOUR'])
    change = '{:,.4f}'.format(data['CHANGEPCT24HOUR'])
    formatted = {}
    formatted['title'] = '{}: ${} ({}%)'.format(ticker.upper(), price, change)
    formatted['subtitle'] = '24hr high: ${} | 24hr low: ${}'.format(high, low)
    return formatted


def main(wf):
    # Get query from Alfred
    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    if query:
        url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + \
            query.strip().upper() + '&tsyms=USD'
        r = web.get(url)
        # throw an error if request failed
        # Workflow will catch this and show it to the user
        r.raise_for_status()
        result = r.json()
        try:
            formatted = format_strings_from_quote(query, result)
            wf.add_item(title=formatted['title'],
                        subtitle=formatted['subtitle'],
                        arg='https://www.cryptocompare.com/coins/' + query + '/overview/USD',
                        valid=True,
                        icon=ICON_WEB)
        except:
            wf.add_item(title='Couldn\'t find a quote for that symbol.',
                        subtitle='Please try again.',
                        icon=ICON_ERROR)
    else:
        url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,CKB&tsyms=USD'
        r = web.get(url)
        # throw an error if request failed
        # Workflow will catch this and show it to the user
        r.raise_for_status()
        result = r.json()
        formatted = format_strings_from_quote('BTC', result)
        wf.add_item(title=formatted['title'],
                    subtitle=formatted['subtitle'],
                    arg='https://www.cryptocompare.com/coins/btc/overview',
                    valid=True,
                    icon='icon/btc.png')

        formatted = format_strings_from_quote('ETH', result)
        wf.add_item(title=formatted['title'],
                    subtitle=formatted['subtitle'],
                    arg='https://www.cryptocompare.com/coins/eth/overview',
                    valid=True,
                    icon='icon/eth.png')

        formatted = format_strings_from_quote('CKB', result)
        wf.add_item(title=formatted['title'],
                    subtitle=formatted['subtitle'],
                    arg='https://www.cryptocompare.com/coins/ckb/overview',
                    valid=True,
                    icon='icon/ckb.png')

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
