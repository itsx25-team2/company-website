# Amin Mahamoud - Personlig Dokumentationsyta

Denna mapp används för Amins individuella anteckningar, arbetssammanfattningar
och defensiva analyser i projektet.

Dokumentera datum, genomfört arbete, verifiering, egna slutsatser och nästa
steg. Lägg aldrig in credentials, privata nycklar, tokens eller flaggvärden.

## Uppföljning 2026-09-24

Amin var inte närvarande under dagens arbete med Workshop 3.5-4. Den gemensamma
tekniska setupen är genomförd och ska inte installeras om.

### Aktuell status

- `company-website.team2.arpa` fungerar via Headscale MagicDNS och Kubernetes
  Ingress.
- Applikationen svarar med HTTP `200` och har `1/1` redo repliker.
- GitHub Actions bygger, signerar och driftsätter images med en oföränderlig
  digest.
- Cosign-policyn nekar osignerade images och godkänner Team 2:s signerade image.
- Rollback till föregående signerad version och återställning till senaste
  versionen är verifierade.
- APP-08 och APP-09 samt Issues #3 och #9 är avslutade.

### Börja här

| Dokument | Syfte |
| --- | --- |
| [Projektets README](../../README.md) | Arkitektur, arbetsflöde och aktuell status. |
| [Workshopstatus](../../docs/workshop3_setup_status.md) | Teknisk setup och verifiering. |
| [Teamsammanfattning 2026-09-24](../../docs/team_work_summary_2026-09-24.md) | Dagens arbete med Ingress, images, Cosign och rollback. |
| [Produktbacklog](../../docs/product_backlog.md) | Klara och återstående uppgifter. |
| [Gemensam anslutningsguide](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/docs/gemensam_anslutningsguide.md) | Tailscale, Headscale, SSH, MagicDNS och felsökning. |
| [Amins infra-mapp](https://github.com/itsx25-team2/kurs6-team2-infra/tree/main/members/aminmahamoud-arch) | Tidigare uppföljning och instruktioner. |

### Personlig kontrollista

1. Synka `main` i både infra- och applikationsrepot.
2. Starta Tailscale och aktivera annonserade routes samt Tailscale DNS.
3. Kontrollera att den egna enheten syns i Tailnet.
4. Verifiera `company-website.team2.arpa` från den egna datorn.
5. Dokumentera den egna verifieringen och eventuella problem i denna mapp.

Ändra inte den delade infrastrukturen direkt för att komma ikapp. Skapa ett
Issue och arbeta via egen branch och pull request om en gemensam ändring
behövs.
