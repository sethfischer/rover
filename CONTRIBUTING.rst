============
Contributing
============

Images
------

Add appropriate metadata. For raster images add EXIF metadata:

.. code-block:: bash

    #!/usr/bin/env bash

    exiftool \
        -overwrite_original \
        -Artist="FirstName LastName" \
        -AttributionName="FirstName LastName" \
        -AttributionURL="https://example.com" \
        -Comment="Short description" \
        -Description="Long description." \
        -License="https://spdx.org/licenses/MIT.html" \ # SPDX license URL
        -Rights="MIT" \  # SPDX identifier
        -UsageTerms="Copyright YYYY FirstName LastName" \
        image.jpeg
