# Rotation av Headscale API-nyckel

## Syfte

GitHub Actions använder en tidsbegränsad Headscale API-nyckel för att skapa
en kortlivad, icke återanvändbar pre-auth key inför varje deployment. Den
kortlivade nyckeln ansluter runnern till Team 2:s privata nät och försvinner
när den tillfälliga noden tas bort.

Detta är skilt från GCP och Cosign:

- GCP-autentisering använder WIF och kräver ingen Service Account Key.
- Cosign använder GitHub OIDC för nyckellös signering.
- Headscale saknar koppling till GitHub OIDC i vår nuvarande lösning och
  behöver därför en separat API-nyckel i GitHub Secrets.

## Ansvar och giltighet

- Team 2:s administratörer ansvarar gemensamt för rotationen.
- Nyckeln lagras endast som GitHub Secret `HEADSCALE_API_KEY`.
- Normal giltighetstid är 30 dagar.
- Utgångsdatum kontrolleras minst en vecka före planerad deployment.
- Nyckelvärden eller fullständiga prefix får aldrig visas, dokumenteras,
  skickas i chatt eller lagras i Git.

## Kontroll före rotation

Anslut till jumphosten med personlig OS Login-identitet och lista metadata:

```bash
sudo headscale apikeys list
```

Listan används endast för ID, skapandedatum och utgångsdatum. En röd eller
passerad tid betyder att nyckeln inte längre kan skapa pre-auth keys.

## Säker rotation

Kör från en administratörs lokala terminal. Anpassa projekt, zon och
instansnamn om infrastrukturen ändras:

```bash
set -euo pipefail

NEW_KEY="$(
  gcloud compute ssh team2-jumphost \
    --project=itsx25-lab \
    --zone=europe-north2-b \
    --tunnel-through-iap \
    --quiet \
    --command='sudo -n headscale apikeys create --expiration 720h' \
  | tr -d '\r\n'
)"

case "$NEW_KEY" in
  hskey-api-*) ;;
  *) unset NEW_KEY; echo "Rotation misslyckades" >&2; exit 1 ;;
esac

printf '%s' "$NEW_KEY" \
  | gh secret set HEADSCALE_API_KEY \
      --repo itsx25-team2/company-website
unset NEW_KEY
```

Nyckeln hålls endast tillfälligt i processens minne och skrivs inte ut.
Kontrollera därefter endast att GitHub visar ett nytt uppdateringsdatum:

```bash
gh secret list --repo itsx25-team2/company-website \
  | rg '^HEADSCALE_API_KEY'
```

## Verifiering

1. Starta deploymentworkflowen från `main`.
2. Kontrollera att `Generate Ephemeral Headscale Key` lyckas.
3. Kontrollera att runnern når K3s API genom Headscale.
4. Kontrollera att Kubernetes-rollouten lyckas.
5. Verifiera `/healthz`, antal redo repliker och deployad image-digest.
6. Verifiera Cosign-signaturen och SBOM-attesteringen.

Återkalla en gammal nyckel först när den nya är verifierad:

```bash
sudo headscale apikeys expire --id GAMMALT_ID
```

Använd ID från `headscale apikeys list`. Klistra aldrig in själva
nyckelvärdet i kommandot eller dokumentationen. Redan utgångna nycklar kan
ligga kvar som revisionsspår men kan inte längre användas.

## Felsökning

Exit code `22` från `curl` i steget `Generate Ephemeral Headscale Key`
betyder att Headscale returnerade ett HTTP-fel. Kontrollera i denna ordning:

1. API-nyckelns utgångsdatum.
2. Att GitHub Secret nyligen uppdaterats.
3. Att `HEADSCALE_URL` fortfarande pekar på rätt server.
4. Att `HEADSCALE_USER_ID` avser CI-användaren.
5. Headscale-tjänstens status och loggar utan att skriva ut credentials.

En misslyckad deployment ersätter inte automatiskt den körande podden. Gör
alltid en separat healthcheck för att skilja deploymentfel från driftavbrott.
