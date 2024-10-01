import requests
import json

url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

payload = json.dumps({
  "model": "GigaChat",
  "messages": [
    {
      "role": "user",
      "content": "Нарисуй солнце. Формат jpg"
    }
  ],
  "stream": False,
  "repetition_penalty": 1
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.RQ7VPo_hs7ZMyucmNFqpiNuB1p4FjZZL4WOzJ_T8x6zMSsaAMXwt2LCKqcglTK9_E1zydcNK12-AcrkMB_kbMIe-EVbvCcfn_kMHVdJcOOzTO0Iz_CirDiO484DY-zuL5SXjAapOQcnlDT0ucwpEJTVwMwbirEWkUvq7pGutCz9Frp5UGnKCLC6EFyLv6obX3VqxUthcg0MuDu1SBcbNzfXkOGd6Dod9cEbpgO0_NiZjMA9g7Sh0fwqCnLL4unP67eFcB2bEEuldqWuL6b5Xn8yMBJNnimi9GCx4dqUqpMAsqHBxfJipjaRQewoakIZyz6AsReFy375TrwdKtA4q5w.l5qJfPEClFUEvVrQfFXWWQ.44oKlhAFGbgpGzPegmIvDsv6sXW_oSTKK2RDojpR1bgAqKljQD3RzU0-rtVI3zglopsFVYQce81AJ6bZ0_VJkymEx89zg7vALGz7aITtdkR06B7KX9okJlD_vKKfufrd3AzOY0urOnT0DinZpuTcWNHZgPX06trMsZ-avxH0B9efrjEW7R1ey25YBKyI-g4fFA2MO8wFr_D5vshk9JC05zBhe01vxQ8j5GcwsuLYD0bthg9E9Yn1Ld7kulNdcihQ2-IjwsMrCItsCV1FiIeDqS_hTbhpvM84tMcsYhqAONuV3eqw-H1seBVxbJYvUaehLJ2uSTRZtlOFlX6xVyd42e18efpnZOwFabY6oVUbtLQbLQ-_TDtG8-ETHM_8XbECqbSg4bHb0rTfnXWDJ3GiezZqZvYtxdh9pgKOuQ3culX-XVlEAzIm-BPWv1aZBdZnv7yCOBgD7ymzXRU0iiOsTGgg4WcgoTC3jpbW4iIGqfTVnoUER0VyChtVx-GR875t57hXxOA3alpbmrR4sWQUSlNsm5zQcSxUfKepQPuMz3u4H2skRDFhQkAnInnh6juZzROV8sIsURUG3V_8h_NNOxgFoDWWVEceT9FrfBkBVrbLJjsVEjJ-PZ_kTaaZ8KUvedzRQmmfO_-OT4jBipY1zYzdsy-z4a3PLYLvupJ3cYX1v2LG8uuyvmlyptKGEWaShUrwNHq9ziMVurOR6tRPdbfn6le1lx6stZff0TfZfoY.t-kZPntq1TqckNFXs5dUpU-XU2AR0DeWcEXAkp3mbwY'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False, cert=None)

print(response.text)
