UPDATE users
SET internal_notes = NULL
WHERE internal_notes IN (
    'pwned',
    'Remember to rotate the dev-secret-key before production. Also, the staging DB password is staging123.',
    'Password vault backup location: /opt/vault/backup.zip',
    'ITSX25{this_is_a_second_placeholder}',
    'Secret project codename: Phoenix. Repo is hidden under /internal/phoenix.git',
    'Admin panel mockups are in /shared/admin_v2.fig. Still using the old FTP server.'
);