import fut
import time
import math
import multiprocessing as mp

def watch(q, api, defIds, length=1200):

    api.resetSession()
    trades = {}

    if not isinstance(defIds, (list, tuple)):
        defIds = (defIds,)

    for defId in defIds:
        trades[defId] = {}

        for i in range(0,5):
            stop = False
            # Look for any trades for this card and store off the tradeIds
            for item in api.searchAuctions('player', defId=defId, start=i*50+1, page_size=50):
                # 20 minutes should be PLENTY of time to watch for trends
                if item['expires'] > length:
                    stop = True
                    break

                trades[defId][item['tradeId']] = item

            if stop:
                break

    # need to have trades to continue
    if not len(trades):
        return

    # Watch these trades until there is no more to watch or we get a termination
    expired = False
    while not expired:
        expired = True

        for defId in trades.keys():
            # update trade status
            for item in api.tradeStatus(list(trades[defId].keys())):
                trades[defId][item['tradeId']] = item
                if item['expires'] > 0: expired = False

            # start calculations
            lowest = 0
            median = 0
            mean = 0
            minUnsoldList = 0

            activeTrades = {k:v for (k,v) in trades[defId].items() if v['currentBid'] > 0}
            if len(activeTrades):
                activeBids = [v['currentBid'] for (k,v) in activeTrades.items()]
                activeBids.sort()
                lowest = min(activeTrades[k]['currentBid'] for k in activeTrades)
                median = activeBids[math.floor((len(activeBids)-1)/2)]
                mean = int(sum(activeTrades[k]['currentBid'] for k in activeTrades) / len(activeTrades))

            expiredNotSold = {k:v for (k,v) in trades[defId].items() if v['currentBid'] == 0 and v['expires'] == -1}
            if len(expiredNotSold):
                minUnsoldList = min(expiredNotSold[k]['startingBid'] for k in expiredNotSold)

            q.put({
                'defId': defId,
                'total': len(trades[defId]),
                'active': sum(trades[defId][k]['expires'] > 0 for k in trades[defId]),
                'bidding': len(activeTrades),
                'lowest': lowest,
                'median': median,
                'mean': mean,
                'minUnsoldList': minUnsoldList
                })