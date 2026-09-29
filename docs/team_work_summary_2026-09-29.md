# Team 2 - arbetssammanfattning 2026-09-29

## Närvaro

- Närvarande: Jonny Nguyen, Fajk Zhupa, Tim Rundquist, Lars Torngren och Wilibroad Ngebi.
- Frånvarande: Amin Mahamoud.

## Dagens mål

Teamet följde upp Workshop 3.5-4 och Workshop 4 efter merge och deployment.
Fokus låg på att kontrollera dokumenterad status, driftsättning och
applikationens e-postsignatur utan att ändra data i live-miljön.

## Verifierad status

- Workshop 3.5-4:s DNS-, Ingress-, digest-, Cosign- och policyflöde är
  dokumenterat och verifierat.
- Workshop 4:s SBOM, attestering, signering och säkerhetshärdning är
  integrerade.
- OS Login-loggar visade policykontroller för `team2-jumphost` och
  `team2-primary`.
- En isolerad lokal container verifierade tillåtna och otillåtna
  platshållare utan att använda teamets databas.
- Samma användarflöde verifierades manuellt i live-miljön utan att några
  profiländringar sparades.
- Live `/healthz` gav HTTP `200`, status `healthy` och ansluten databas.
- PR #22 mergades som `64bb55f`.
- Deployment `36565389383` efter merge slutfördes med resultatet `success`.
- Den deployade imagen är låst till digest `sha256:bf1b2a60...`.
- Parallellt mergades Lars Torngrens
  [infra-PR #77](https://github.com/itsx25-team2/kurs6-team2-infra/pull/77). Han
  dokumenterade hur han hittade de två nya flaggorna i den uppdaterade
  kursapplikationen.
  Sammanfattningen återger varken flaggvärden eller angreppskommandon.

## Observationer

Live-miljön använder ett självsignerat TLS-certifikat, vilket är accepterat i
kursens interna labb men ska inte förväxlas med en publikt betrodd
produktionslösning. Lokal WSL hade ingen Kubernetes-kontext konfigurerad.
Klustret verifierades i stället genom GitHub Actions och applikationens
live-kontroller. Direkt SSH nekades eftersom den lokala publika nyckeln inte
accepterades. Detta hindrade inte verifieringen av applikationens interna
labbflöde.

## Säkerhet

Inga lösenord, sessionsvärden, tokens, nycklar eller flaggvärden
dokumenterades. Inga data sparades eller administrativa resurser ändrades
under live-testet.

## Nästa steg

- Fortsätt den defensiva analysen inom godkänd kursscope.
- Följ upp öppna Issues och dokumentera nya observationer utan hemligheter.
- Åtgärda den lokala OS Login-/SSH-vägen separat om direkt administration
  från arbetsstationen behövs.
