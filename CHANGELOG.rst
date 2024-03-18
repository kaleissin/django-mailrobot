Changelog
=========

0.8.1
-----

Stops importing ugettext_lazy, which was removed in Django 4.0. This is only
used in the admin, but our additions to the admin has no tests.


0.8.0
-----

Adds support for Django 4.2 and 5.0.

Drops support for Django older than 3.2.

Adds support for Python 3.10, 3.11 and 3.12.

Drops support for Python older than 3.8.

More modernizing of package building and testing.

Last version to support Django 3.2.

0.7.0
-----

Adds support for Django 3.2.

Drops support for Django 2.2 or older, as well as Python 3.5 or older.

Shims to support Python 2.x and Django < 3.2 have been removed.

Sundry modernizing of package building and testing.


0.6.0
-----

Adds support for Django 2.2.

Last version to support Python 2 and Django's 2.2 and older.
