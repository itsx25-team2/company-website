# Team 2 - arbetssammanfattning 2026-10-06

## Närvaro

- Närvarande: Jonny Nguyen, Fajk Zhupa, Lars Torngren, Tim Rundquist och
  Wilibroad Ngebi.
- Frånvarande: Amin Mahamoud.

## Dagens mål

Målet var att följa upp den mergade hardeningen av company-website och
verifiera att den fungerar i drift utan att skapa nya risker eller ändra
produktionsmiljön manuellt.

## Genomfört arbete

1. PR #32 granskades. Den inför non-root-körning, skrivskyddat rotfilsystem,
   initcontainer för data-rättigheter och `Recreate` för SQLite-volymen.
2. GitHub Actions kontrollerades. Både `Application Checks` och deploymenten
   på `main` avslutades framgångsrikt.
3. Live-miljön verifierades via `company-website.team2.arpa`. Startsidan och
   `/healthz` svarade med HTTP `200`, och health-checken rapporterade ansluten
   databas.
4. Ett normalt profilflöde kontrollerades manuellt med ett tilldelat testkonto
   i utbildarens kursmiljö: spara, omladdning samt ut- och inloggning
   fungerade. Testvärdet
   återställdes efter kontrollen.
5. Profilformuläret kontrollerades så att serverstyrda fält inte är
   redigerbara. `Internal Notes` visas skrivskyddat för profilägaren men inte
   för andra användare enligt den aktuella behörighetskontrollen.
6. Den fullständiga lokala testsviten gav `22 passed`. Fyra riktade
   säkerhetstester för profilbehörighet och avstängda konton gav `4 passed`.
7. Den gemensamma MITRE/TI/TLP-sammanställningen uppdaterades med dagens
   verifierade evidens, utan hemligheter eller användardata.

## Resultat

- Den aktuella deploymenten är frisk och applikationen fungerar för ett
  vanligt användarflöde efter hardeningen.
- Datavolymens rättigheter fungerar tillsammans med en rootlös
  applikationsprocess.
- Automatiska tester bekräftar att användare inte kan ändra andra användares
  profiler eller skriva över serverstyrda profilfält.
- Teamet behöver besluta om `Internal Notes` ska fortsätta vara läsbart för
  profilägaren eller endast vara tillgängligt för administratörer.
- `Recreate` är en medveten begränsning för SQLite med `ReadWriteOnce`:
  strategin undviker volymkonflikt, men ger ett kort avbrott vid rollout.

## Nästa steg

- Låt teamet granska dagens dokumentation innan den commitas och skickas som
  pull request.
- Håll den nya verifieringsnotisen uppdaterad när profilflöde, databas eller
  deploymentstrategi ändras.
- Utvärdera extern databas om applikationen senare behöver flera repliker eller
  avbrottsfria deploymenter.
- Fortsätt arbetet med öppna backlogpunkter, särskilt reproducerbar
  dokumentation av Trivy/Discord-kontrollen.

## Säkerhet

Inga lösenord, cookies, tokens, nycklar, webhookar eller känsliga
runtime-detaljer har lagts i denna sammanfattning.
