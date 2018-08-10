# cpr_udtraek
NOT WORKING AT THE MOMENT!

Besked:
Vær opmærksom på, at programmet er ikke helt færdigt, eller testet ordentligt. Det blev udviklet ifm. et projekt, men er endnu ikke blevet taget i brug.
Programmet kan oprette en sftp-forbindelse, hente- og parse hændelsdata filer til dictionaries.
Fordi der har været interesse for koden, så har jeg nu valgt at lægge den her på GitHub. Og forhåbentlig får jeg, eller en anden, mulighed for lige at nusse koden lidt.

Output eksempel:

```
{
  '0123456789' : {
                    record_001: {
                      'key': 'value',
                      'key': 'value',
                      'key': 'value',
                      ...
                    },
                    record_002: {
                      'key': 'value',
                      'key': 'value',
                      ...
                    },
                    ...
  },
  '9876543210' : {
                    record_001: {
                      'key': 'value',
                      'key': 'value',
                      'key': 'value',
                      ...
                    },
                    record_002: {
                      'key': 'value',
                      'key': 'value',
                      ...
                    },
                    ...
  },
}
```
