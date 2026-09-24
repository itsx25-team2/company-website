# Individuell arbetssammanfattning - Jonny Nguyen - 2026-09-24

## Dagens mål

Målet var att slutföra Workshop 3.5-4 genom att göra applikationen åtkomlig
via ett internt DNS-namn, ersätta direkt användning av port 80 med Kubernetes
Ingress och förbättra spårbarheten och säkerheten i deploymentflödet.

## Mitt arbete

Jag arbetade stegvis i både infra- och applikationsrepot:

1. Jag verifierade att Headscale MagicDNS var aktivt och att
   `company-website.team2.arpa` pekade på Team 2:s primary-server.
2. Jag kontrollerade åtkomsten från min egen klient via Tailscale och fick
   HTTP `200` utan lokal hosts-fil eller webbläsarproxy.
3. Jag deltog i arbetet med Helm och `ingress-nginx` samt analyserade
   portkonflikten som uppstod när både applikationen och Ingress använde port
   80 på samma nod.
4. Jag tog bort behovet av `hostPort`, lade till ett Ingress-manifest och
   säkerställde att GitHub-deployern hade nödvändig RBAC-behörighet.
5. Jag förbättrade pipelinen så att images får både `latest` och en
   commitbaserad tagg, medan Kubernetes driftsätter en oföränderlig digest.
6. Jag lade till en commit-label i poddmallen för att kunna koppla en körande
   deployment till rätt Git-commit.
7. Jag lade till nyckellös Cosign-signering med GitHub OIDC och verifierade
   signaturen oberoende.
8. Jag verifierade image-policyn genom att kontrollera att en osignerad
   testimage nekades och att Team 2:s signerade image godkändes.
9. Jag genomförde ett kontrollerat rollback-test till föregående signerade
   digest och återställde därefter den senaste signerade versionen.

## Verifierat resultat

- MagicDNS-namnet löser till rätt intern adress.
- Ingress routar `company-website.team2.arpa` till applikationen.
- Applikationen svarar med HTTP `200`.
- Deploymenten har `1/1` redo repliker.
- GitHub Actions bygger, signerar och driftsätter imagen framgångsrikt.
- Osignerade images nekas i det skyddade namespace som policyn omfattar.
- Både rollback-versionen och den återställda versionen blev redo och svarade
  med HTTP `200`.
- Issue #3 och APP-08 är avslutade efter verifierad rollback.

## Vad jag lärde mig

MagicDNS löser namnet, men Ingress avgör vilken Kubernetes Service som ska ta
emot en HTTP-förfrågan. De två funktionerna kompletterar alltså varandra.

En image-tagg som `latest` kan flyttas och är därför inte tillräcklig för en
säker rollback. En digest identifierar exakt den artefakt som ska köras.
Cosign-signaturen ger dessutom ett verifierbart samband mellan imagen och
Team 2:s godkända GitHub Actions-workflow.

Rollback är inte färdigtestad bara för att Kubernetes accepterar kommandot.
Jag kontrollerade därför rollout-status, antal redo repliker och HTTP-svar,
och återställde sedan den senaste versionen med samma kontroller.

## Säkerhet och avgränsning

Arbetet genomfördes i Team 2:s godkända kursmiljö. Inga credentials, tokens,
privata nycklar eller flaggvärden dokumenterades. Endast förkortade publika
image-digests används i sammanfattningen.

## Relaterad dokumentation

- [Teamsammanfattning 2026-09-24](../../docs/team_work_summary_2026-09-24.md)
- [Workshopstatus](../../docs/workshop3_setup_status.md)
- [Produktbacklog](../../docs/product_backlog.md)
- [Gemensam anslutningsguide i infra-repot](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/docs/gemensam_anslutningsguide.md)
