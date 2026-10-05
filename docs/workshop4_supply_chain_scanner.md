# Workshop 4 - Supply Chain Security Scanner

**Klassificering:** TLP:CLEAR (sanerad dokumentation för det publika repot)

## Syfte

Den här kontrollen ska ge teamet återkommande information om
supply-chain-risker i Kubernetes-miljön. Trivy skannar enligt en schemalagd
Kubernetes-körning och resultatet skickas till teamets Discord-kanal.

## Verifierad driftstatus

Fajk har bekräftat följande arbete i Team 2:s K3s-miljö:

1. En Discord-webhook skapades för rapportering.
2. Webhookens värde sparades som en Secret på produktionsservern. Värdet har
   inte dokumenterats i Git eller i den här filen.
3. Kubernetes-RBAC skapades för skannerns service account.
4. Ett schemalagt Kubernetes-jobb med Trivy applicerades i K3s.
5. En manuell engångskörning testades. Resultatet nådde Discord via webhooken.

Detta är driftbevis för att kontrollen fungerar. Det är dock inte samma sak som
att den är reproducerbar från repot.

## Spårbarhet och begränsning

- [PR #25](https://github.com/itsx25-team2/company-website/pull/25) mergades
  med dokumentation om Trivy och Discord.
- PR #25 innehåller endast denna dokumentation; den innehåller inte
  Kubernetes-manifest för CronJob, RBAC eller Secret.
- Infra-repots PR #78 återger det genomförda driftarbetet och den manuella
  testkörningen.
- Den versionerade dokumentationen räcker därför för att förstå syftet och
  statusen, men inte för att återskapa eller granska den fullständiga
  Kubernetes-installationen enbart från Git.

## Säkerhetsbedömning

Kontrollen ger ett defensivt lager mot supply-chain-risker. Den ersätter inte
befintliga skydd som signerade images, SBOM/attestering och policykontroll.

RBAC behövs för att skannern ska kunna läsa det den ska analysera, men
behörigheterna bör granskas mot principen om minsta privilegium. Webhooken ska
fortsätta lagras som en hemlighet utanför Git.

## Rekommenderad fortsattning

1. Dokumentera ägare, körschema, vad som skannas och vilka larm som ska följas
   upp.
2. Versionshantera icke-hemliga Kubernetes-manifest eller IaC efter review.
3. Behåll webhookvärdet enbart i Secret-hantering och dokumentera rotation och
   återkallning utan att visa värdet.
4. Granska RBAC med fokus på minsta privilegium.
5. Dokumentera en säker återställningsrutin för kontrollen.

## Säkerhet

Den här filen innehåller inga webhookvärden, tokens, Kubernetes-hemligheter,
interna IP-adresser eller råa skannerrapporter.

