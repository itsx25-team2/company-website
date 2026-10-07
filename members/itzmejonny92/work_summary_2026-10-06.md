# Individuell arbetssammanfattning - Jonny Nguyen - 2026-10-06

## Fokus

Jag följde upp den mergade hardeningen av company-website efter PR #32. Målet
var att kontrollera att säkerhetsförbättringarna fungerar både för en vanlig
användare och i den driftsatta Kubernetes-miljön.

## Genomfört arbete

1. Jag gick igenom PR #32 och dess ändringar i Dockerfile,
   `k8s/deployment.yaml` och deploy-workflowet.
2. Jag kontrollerade GitHub Actions. Applikationstesterna och deploymenten på
   `main` var gröna.
3. Jag verifierade att `company-website.team2.arpa` svarade med HTTP `200` och
   att `/healthz` rapporterade ansluten databas.
4. Jag använde ett tilldelat testkonto i utbildarens kursmiljö för en ofarlig
   profiländring. Ändringen sparades, fanns kvar efter omladdning och fanns
   fortfarande kvar efter ut- och inloggning. Därefter återställde jag
   testvärdet.
5. Jag kontrollerade att profilformuläret inte gör de serverstyrda fälten
   `role` eller `internal_notes` redigerbara. `Internal Notes` visas
   skrivskyddat i den testade profilens egen vy men inte när andra användares profiler
   visas.
6. Jag körde den fullständiga lokala testsviten med resultatet `22 passed`
   samt fyra riktade tester för profilbehörighet och avstängda konton med
   resultatet `4 passed`.
7. Jag uppdaterade MITRE/TI/TLP-sammanställningen med en sanerad
   verifieringsnotis för dagens resultat.

## Resultat och pedagogisk slutsats

PR #32 kombinerar tre kontroller som behöver fungera tillsammans:

- Initcontainern förbereder SQLite-volymens filrättigheter.
- Applikationen kör sedan som en separat, icke-root-användare.
- Rotfilsystemet är skrivskyddat medan endast den avsedda datavolymen och
  `/tmp` är skrivbara.

Den manuella kontrollen visar användarperspektivet: profilen kan uppdateras
och sparas. Testsviten visar serverperspektivet: en användare kan inte ändra
någon annans profil eller skicka in serverstyrda fält. Profilvyn returnerar
inte en annan användares interna anteckningar. Health-checken visar
driftperspektivet: applikationen och databasen svarar i den aktuella
deploymenten.

Att anteckningarna visas skrivskyddat för profilägaren är ett medvetet beteende
i den aktuella koden. Teamet behöver ändå ta ställning till om namnet
`Internal Notes` innebär att fältet i stället ska vara administratörsexklusivt.

## Kvarvarande begränsning

Applikationen använder SQLite på en `ReadWriteOnce`-volym. Deploymenten
använder därför strategin `Recreate` för att undvika att två poddar samtidigt
använder databasfilen. Det kan ge ett kort avbrott vid rollout. En extern
databas är ett långsiktigt förbättringsspår om applikationen behöver fler
repliker eller avbrottsfria deploymenter.

## Säkerhet och avgränsning

- Inga lösenord, sessionscookies, tokens eller andra hemligheter
  dokumenterades.
- Testet utfördes endast med ett tilldelat testkonto i utbildarens kursmiljö
  och en ofarlig profiländring som återställdes efter kontrollen.
- Ingen Kubernetes-resurs, databas eller produktionskonfiguration ändrades
  manuellt under verifieringen.

## AI-användning

Jag använde OpenAI Codex för pedagogiska förklaringar, läsande statuskontroller
och förslag till dokumentationsstruktur. Jag genomförde själv den manuella
kontrollen i webbläsaren och bedömde resultatet mot applikationens beteende,
tester, GitHub Actions och driftstatus.
