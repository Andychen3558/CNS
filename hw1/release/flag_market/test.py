#!/usr/bin/env python2

import os
import sys
import base64
import random
import hashlib


def sha256(data):
    m = hashlib.sha256()
    m.update(data)
    return m.hexdigest()

def intro():
    print '==============================='
    print '          Flag Market          '
    print '==============================='
    print '   1. Check balance            '
    print '   2. Buy BALSN coin           '
    print '   3. Buy Flag                 '
    print '   4. Exit                     '
    print '==============================='

def init():
    sys.dont_write_bytecode = True
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdin = os.fdopen(sys.stdin.fileno(), 'r', 0)

    KEY = os.urandom(random.randint(40, 50))
    assert len(KEY) >= 40 and len(KEY) <= 50

    return KEY, 100

def check_balance(balance):
    print 'You have ${}.'.format(balance)
    return

def buy_coin(KEY, balance):
    print '--------------------------'
    print '    $5 -> 1 BALSN coin    '
    print '--------------------------'
    print 'How many BALSN coin you want?'
    num = raw_input('> ').strip()

    try:
        num = int(num)
    except:
        print 'Something is wrong...'
        return balance

    if num <= 0:
        print "You are so funny..."
        return balance

    if num * 5 > balance:
        print "You don't have enough money!"
        return balance

    balance -= num * 5
    balsn_coin = sha256('key={}&BALSN_Coin={}'.format(KEY, num))
    print 'You bought {} BALSN coin!'.format(num)
    print 'Show this token to buy flag!'
    print 'Token: ' + balsn_coin

    return balance

def buy_flag(KEY):
    print '-------------------------------'
    print '    1000 BALSN coin -> FLAG    '
    print '-------------------------------'

    token = 1
    msg = "key=1wdqq&BALSN_Coin=2147483648&hidden_flag="
    ans = ['{0}'] * 5
    min_bytes = [200] * 5

    for attr in dir(''):
        index = 0
        tmp = '{.' + attr + '.__doc__}'
        for c in tmp.format(''):
            #print(c)
            if  c == '!' and len(attr+str(index)) < min_bytes[0]:
                ans[0] = '{0.' + attr + '.__doc__[' + str(index) + ']}'
                min_bytes[0] = len(attr+str(index))
            elif  c == ';' and len(attr+str(index)) < min_bytes[1]:
                ans[1] = '{0.' + attr + '.__doc__[' + str(index) + ']}'
                min_bytes[1] = len(attr+str(index))
            elif  c == 'P' and len(attr+str(index)) < min_bytes[2]:
                ans[2] = '{0.' + attr + '.__doc__[' + str(index) + ']}'
                min_bytes[2] = len(attr+str(index))
            elif  c == '%' and len(attr+str(index)) < min_bytes[3]:
                ans[3] = '{0.' + attr + '.__doc__[' + str(index) + ']}'
                min_bytes[3] = len(attr+str(index))
            elif  c == '*' and len(attr+str(index)) < min_bytes[4]:
                ans[4] = '{0.' + attr + '.__doc__[' + str(index) + ']}'
                min_bytes[4] = len(attr+str(index))
            index += 1
    tmp = ""
    for a in ans:
        tmp += a
    print(tmp)
    print(min_bytes)
    print(tmp.format(''))
    print(len(tmp))
    msg += tmp

    if sha256(msg) != token:
        print 'Valid Token'

        data = {}
        try:
            for m in msg.split('&'):
                data[m.split('=')[0]] = m.split('=')[1]
        except:
            print 'Something is wrong...'
            return

        try:
            balsn_coin = int(data['BALSN_Coin'])
        except:
            print 'Something is wrong...'
            return

        if balsn_coin < 1000:
            print 'Not enough BALSN coin'
        else:
            print 'Here is your flag!'
            print "FLAG"

            if balsn_coin > 2147483647:
                if 'hidden_flag' in data:
                    hidden = data['hidden_flag'][:111]
                    for c in "!;P%*":
                        if c in hidden:
                            return
                    print(hidden)
                    hidden = hidden.format('')
                    print(hidden)
                    if hidden == "!;P%*":
                        print 'Nice!'
                        print "HIDDEN_FLAG"
    else:
        print 'Invalid Token'

    return

def main():
    KEY, balance = init()

    while True:
        intro()
        choice = raw_input('Command > ').strip()

        if choice == '1':
            check_balance(balance)
        elif choice == '2':
            balance = buy_coin(KEY, balance)
        elif choice == '3':
            buy_flag(KEY)
        elif choice == '4':
            print 'Bye~'
            exit(1)
        else:
            print 'Unknown command'

if __name__ == '__main__':
    main()
