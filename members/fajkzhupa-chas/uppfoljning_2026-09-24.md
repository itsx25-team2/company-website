# Uppföljning för Fajk Zhupa - 2026-09-24

## Bakgrund

Fajk var inte närvarande under dagens arbete med Workshop 3.5-4. Den tekniska
setupen är genomförd och verifierad av gruppen. Detta dokument sammanfattar
vad som ändrades och vad Fajk behöver kontrollera på sin egen klient.

## Genomfört arbete

- Headscale MagicDNS har posten `company-website.team2.arpa -> 10.0.2.3`.
- Helm och `ingress-nginx` är installerade på Team 2:s primary-server.
- Applikationens `hostPort: 80` har ersatts med Kubernetes Ingress.
- GitHub Actions publicerar `latest`, en commitbaserad tagg och deployar med
  en oföränderlig image-digest.
- Poddmallen märks med aktuell Git-commit för spårbarhet.
- Containerimagen signeras nyckellöst med Cosign och GitHub OIDC.
- Image-policyn nekar osignerade images och godkänner Team 2:s signerade image.
- Rollback till föregående signerad version och återställning till den senaste
  versionen har verifierats med `1/1` redo repliker och HTTP `200`.
- APP-08 och APP-09 samt Issues #3 och #9 är avslutade.

## Det Fajk behöver göra

1. Synka `main` i både `kurs6-team2-infra` och `company-website`.
2. Läs workshopstatusen och teamsammanfattningen via länkarna nedan.
3. Starta Tailscale på den egna klienten och acceptera routes samt Tailscale
   DNS.
4. Kontrollera att `company-website.team2.arpa` går att slå upp och öppna.
5. Dokumentera den egna verifieringen eller eventuella problem i medlemsmappen.

De gemensamma installationerna ska inte göras om. Om något behöver ändras i
den delade miljön ska arbetet börja i ett Issue och göras via egen branch och
pull request.

## Viktiga länkar

- [Projektets README](../../README.md)
- [Workshopstatus](../../docs/workshop3_setup_status.md)
- [Teamsammanfattning 2026-09-24](../../docs/team_work_summary_2026-09-24.md)
- [Produktbacklog](../../docs/product_backlog.md)
- [Gemensam anslutningsguide i infra-repot](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/docs/gemensam_anslutningsguide.md)

## Säkerhet

Lägg aldrig in credentials, tokens, privata nycklar, kubeconfig eller
flaggvärden i repositoryt.
