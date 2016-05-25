===================
Disc Usage Locator
===================

This tool is intended to provide a simple and effective means to locate folders utilizing a large portion of a given disc or filesystem.  It will also provide the ability to save the collected file data as a CSV for further analsis and processing.  A planned enhancemet will be to provide the ability to perform mass deletions or file moves to other locations in order to free up space.

Required Elements
=================

To run the Disc Usage Locator program you will need the source file, disc_usage.py and the image file, check.png, which is used in the directory tree display to indicate selected entries.

How to install
==============

You can either use GIT to clone this repository to your execution environment or download the GIT zip file and extract the identified required files.

.. code:: console

    $ git clone https://github.com/BillSass/is210-Final-DiscUsageLocator


How to execute
==============

The Python program must be invoked from the same folder containing the check.png file (this file must be in the current-working-directory).  The invocation can be through IDLE (run) or via the Python terminal command.  There are no invocation parameters:

.. code:: console

    $ python disc_usage.py

Known Restrictions or Issues
============================

#. Due to time restrictions and for safety reasons, the file Delete and Move actions have not been implemented and so the associated action radio buttons have been disabled.

#. Depending on the number of files and sub-directories under the selected folder is can take several seconds and even a minute or more, before the directory tree display is presented.

#. There is a delay in presenting the "processing" status message on the first dialog window (following Start-ing the directory processing. 

#. Related to the previous issue, when the dialog returns from the directory tree display back to the folder selection dialog, the command buttons, especially Quit, need to be clicked twice.  I have not yet been able to diagnose the cause.

Please let me know if you encounter any other issues.
