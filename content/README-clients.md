# Adding client logos

Two ways, both need no code:

1. **Drop the file in** `src/assets/images/clients/` and name it after the client, lower case, words joined with hyphens:
   `koroboro-international-school.png` (or .svg, .webp, .jpg). The site finds it by the client's name in `clients.json`.
2. **Or name it in `clients.json`**: `"logo": "my-file.png"` (the file can be in `src/assets/images/` or `src/assets/images/clients/`).

Tips: a transparent PNG or an SVG looks best. Aim for a wide logo about 400 px across. Logos show in grey and turn to colour on hover.
A client without a logo shows a neat monogram circle and the name, so you can add logos one at a time.
Only use a logo with the client's permission.
