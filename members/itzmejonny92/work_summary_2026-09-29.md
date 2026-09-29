# Individuell arbetssammanfattning - Jonny Nguyen - 2026-09-29

## Fokus

Jag genomförde en efterkontroll av Team 2:s arbete med Workshop 3.5-4 och
Workshop 4. Målet var att skilja mellan vad som redan var dokumenterat, vad
som fungerade lokalt och vad som faktiskt kunde verifieras i den driftsatta
miljön.

## Status mot workshopparna

Workshop 3.5-4 är genomförd med Headscale DNS-poster, ingress-nginx,
digestlåst deployment, Cosign-signering och policykontroll. Workshop 4 är
genomförd med CycloneDX-SBOM, Cosign-attestering, säkerhetshärdning och
driftsatt applikation.

OS Login-loggarna kontrollerades för `team2-jumphost` och `team2-primary`.
Resultatet visade policykontroller för flera gruppmedlemmar. En policykontroll
är inte samma sak som en unik inloggning, men visar att OS Login har använts i
miljön.

## Lokal funktionskontroll

Jag byggde den aktuella applikationskoden i en isolerad Docker-container med
en tillfällig SQLite-databas och ett lokalt testkonto. Miljön använde ingen
delad volym och påverkade därför inte Kubernetes eller teamets data.

I profilens e-postsignatur verifierade jag att:

- tillåtna platshållare ersattes med rätt profilvärden,
- företagsplatshållaren gav `Placeholder Industries`,
- en okänd platshållare avvisades med ett tydligt fel.

Testcontainern och den tillfälliga databasen togs bort efter kontrollen. Git-
arbetsytan var fortfarande ren.

## Verifiering i live-miljön

Jag upprepade kontrollen i den driftsatta applikationen utan att spara några
profiländringar. Tillåtna platshållare gav rätt värden och en okänd
platshållare gav fel som avsett.

Följande verifierades också:

- `https://company-website.team2.arpa` svarade med HTTP `200`,
- `/healthz` rapporterade `healthy` och ansluten databas,
- rätt inloggningssida och applikation laddades via MagicDNS och Ingress,
- PR #22 mergades som `64bb55f`,
- deployment `36565389383` slutfördes med resultatet `success`.
- den deployade imagen är låst till digest `sha256:bf1b2a60...`.

Det självsignerade TLS-certifikatet krävde ett uttryckligt undantag i
labbmiljön. Lokal WSL hade ingen Kubernetes-kontext konfigurerad. Klustret
verifierades i stället genom GitHub Actions och applikationens live-kontroller.
Direkt SSH till `team2-primary` nekades eftersom den lokala publika nyckeln
inte accepterades. Detta gällde den lokala administrationsvägen;
live-applikationens health-check och användarflöde fungerade.

## Pedagogisk slutsats

Ett lokalt test visar att koden fungerar i en kontrollerad miljö. En
health-check i live-miljön visar att webbservern och databasen svarar. Det
manuella testet efter inloggning visar slutligen att den driftsatta funktionen
fungerar ur användarens perspektiv. Alla tre nivåerna behövdes för att kunna
dra en tydlig slutsats.

## Säkerhet och avgränsning

- Inga lösenord, cookies, tokens eller nyckelvärden dokumenterades.
- Inga profiländringar sparades i live-miljön.
- Ingen databas eller Kubernetes-resurs ändrades manuellt.
- Ingen kod ändrades som del av funktionskontrollen.

## AI-användning

Jag använde OpenAI Codex för pedagogiska förklaringar, statuskontroller och
strukturering av dokumentationen. Jag genomförde den visuella kontrollen i
webbläsaren och bedömde själv resultaten. Uppgifterna verifierades mot repot,
GitHub Actions och den driftsatta kursmiljön.
