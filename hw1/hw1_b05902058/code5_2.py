import os
import random
import time
import base64

if __name__=="__main__":
        ciphers = []
        key_indices = []
        last = ""
        count = 0
        while count < 65:
            ### get the ciphers
            tmp = os.popen("nc 140.112.31.96 10153", 'r').readline()
            random.seed(int(time.time()))
            if tmp == last:
                continue
            else:
                count += 1
                last = tmp
            tmp = list(base64.b64decode(tmp))
            ciphers.append(tmp)

            ### find its key combination
            tmp = random.randint(0,(2**64)-1)
            key_indices.append(tmp)

        end = 0
        for cur in range(64):
            pivot = cur
            while pivot<65:
                if key_indices[pivot] == 0:
                    cand = "".join([chr(i) for i in ciphers[pivot]])
                    if cand.find("BALSN") != -1:
                        print(cand)
                        end = 1
                        break
                if key_indices[pivot] & (2**cur) != 0:
                    key_indices[cur], key_indices[pivot] = key_indices[pivot], key_indices[cur]
                    ciphers[cur], ciphers[pivot] = ciphers[pivot], ciphers[cur]
                    break
                pivot += 1
            if end == 1:
                break
            if pivot == 65:
                continue

            for i in range(cur+1, 65):
                #print(i, key_indices[i])
                if key_indices[i] & (2**cur) != 0:
                    key_indices[i] = key_indices[cur] ^ key_indices[i]
                    ciphers[i] = [ciphers[cur][n]^ciphers[i][n] for n in range(len(ciphers[i]))]
                    if key_indices[i] == 0:
                        cand = "".join([chr(c) for c in ciphers[i]])
                        if cand.find("BALSN") != -1:
                            print(cand)
                            end = 1
                            break
            if end == 1:
                   break
