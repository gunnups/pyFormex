.. $Id$   *- rst -*-

.. |date| date::

===================
Scripts versus Apps
===================
:Date: |date|
:Author: benedict.verhegghe@ugent.be

Introduction
------------

We are currently experimenting with replacing pyFormex *scripts* by *apps*.
For some time we will run both systems together. We hope that this document
will help us to decide in favor of one of the two and that we can then
discard the other.

Because scripts have been an important part of pyFormex right from the start,
we do not want to take this decision lightly. 
While the differences between the two are small as far as the user is concerned,
internally they differ a lot, and there might be glitches that are not obvious
from a first look.

This document there tries to list the differences and the advantages and 
disadvantages of either system. Every deeloper and/or user is encouraged
to add to this document whenever he notes a different behavior between
*scripts* and *apps*.


Scripts
-------

A pyFormex *script* is basically just a piece of Python source code (``.py``).
It is
executed inside pyFormex with an ``exec`` statement. pyFormex provides a
dictionary of global variables to these scripts (the globals of module ``draw``
if the script is executed with the GUI, or those from ``script`` if the script
is executed without GUI). This has the advantage that the first time user has
a lot of functionality without having to know about imports.
Every time the script is executed, the source code has to read, interpreted,
and executed. 


Apps
----

A pyFormex *app* is a Python module. It is usually also provided as Python
source code (``.py``). A module has to be loaded with the ``import`` statement. 
During this loading the source code get compiled to byte code (which is saved
to a ``.pyc`` for faster loading next time) and is kept in memory until
explcitely removed. During the loading of a module the outermost level of code
gets executed, but only the first time (since the loaded module stays in memory,
another ``import`` does not have any effect. It is possible to ``reload`` the
code, but doing that every time you just want to execute some fixed code,
would overthrow some of the main advantages of using modules. Thus, we follow
the normal Python line of thinking: the other level of code is just for 
initialization of the module. The equivalent concept of 'executing a script'
is therefore found in executing some function: if your application defines
a function 'run', this function will get executed automatically when loading
the application, and subsequently also when pushing the 'PLAY' button.

.. raw:: pdf

   PageBreak

Major implications for user
---------------------------

For a user who only executes scripts/apps, the change should have nearly no
implications, because we just need to replace an ``exec`` with a ``run()``.
But since pyFormex users are in most cases also developers of their script/app,
we need to highlight the style differenec in writing one or the other.

A pyFormex script typically looks like this::

  <imports>

  <definitions>
  
  <code to run when executed>
  
  if __name__ == "script"
      <code to run only when executed without GUI>
  
  if __name__ == "draw"
      <code to run only when executed from GUI>


In the new *app* model, this would become::

  from gui.draw import *

  <imports>

  <definitions>
  
  def run():
      <code to run when executed>
  
  <code to initialize the module>


This means that for most scripts, it will suffice to add the line::

  from gui.draw import *

and to put your outermost code inside a function ``run``. 
Then all calls to::

  exit()

should be replaced with::

  return

Finally, make sure that all global variables you assign to in the ``run`` 
method are declared global. Many examples e.g. use a global variable
``dialog``.

Note that a *script* can be structured as an *app* and still be used as
a *script*. Some of the examples in pyFormex are already structured that way.
Indeed, if the initialization code of the *app* contains::
  
  if __name__ == "draw"
      run()

the *app* can not only be run, but also executed as a *script*. Thus transition
to *apps* should be fast and easy. If in the end we decide to keep the *script* 
executor anyway, nothing has been lost by changing your code to the *app* model.

If you have a script that should work both with and without the pyFormex GUI,
you may structure this as follows::

  import pyformex as pf
  if pg.GUI:
     from gui.draw import *
     < DEFINITIONS FOR GUI VERSION >
  else:
     from gui.script import *
     < DEFINITIONS FOR NONGUI VERSION >

  < COMMON DEFINITIONS >

Of course, when your definitions become long it may be better to put them in
separate files::

  import pyformex as pf
  if pg.GUI:
     import myapp_gui
  else:
     import myapp_nongui
  

.. raw:: pdf

   PageBreak

Full comparison
---------------

In favor of *app*:

+-------------------------------------+---------------------------------------+
|         Script                      |            App                        |
+-------------------------------------+---------------------------------------+
| Only source code (.py)              | Source code (.py) or compiled (.pyc). |
|                                     | Code can easily be obscured           |
+-------------------------------------+---------------------------------------+
| Read and interprete on every run    | Read once per session, interprete     |
|                                     | once per lifetime, run many times     |
+-------------------------------------+---------------------------------------+
| Can only import functionality from  | Direct import from any other app.     |
| a script structured as a module.    |                                       |
+-------------------------------------+---------------------------------------+
| Attributes need to be searched and  | The module can have any attributes    |
| decoded from the soure text         |                                       |
+-------------------------------------+---------------------------------------+
| A script can not execute another    | One app can import and run another    |
+-------------------------------------+---------------------------------------+
| It is impossible to run multiple    | It **might** become possible to run   |
| scripts in parallel.                | multiple applications in parallel,    |
|                                     | e.g. in different viewports.          |
+-------------------------------------+---------------------------------------+
| Global variables of all scripts     | Each app has its own globals          |
| occupy single scope                 |                                       |
+-------------------------------------+---------------------------------------+
| Scripts and plugins are two         | Apps and plugins (menus or not) are   |
| different things.                   | both just normal Python modules.      |
+-------------------------------------+---------------------------------------+
| Exit requires special function      | Exit with the normal return statement |
+-------------------------------------+---------------------------------------+
| Canvas settings are global to all   | Canvas settings **could** be made     |
| scripts                             | local to applications                 |
+-------------------------------------+---------------------------------------+
| Data persistence requires export to | Data persistence between invokations  |
| the pyFormex GUI dict PF and reload | is automatic (for module globals)     | 
+-------------------------------------+---------------------------------------+


In favor of *script*:

+-------------------------------------+---------------------------------------+
|         Script                      |            App                        |
+-------------------------------------+---------------------------------------+
| Default set of globals provided     | Everything needs to be imported       |
|                                     | (can be limited to 1 extra line)      |
+-------------------------------------+---------------------------------------+
| Globals of previous scripts are     | Communication between scripts needs   |
| accessible (may be unwanted)        | explicit exports (but is more sound)  |
| (IS THIS STILL TRUE?)               |                                       |
+-------------------------------------+---------------------------------------+
| Users are used to it since longtime | The difference is not large though.   |
+-------------------------------------+---------------------------------------+
| Can be located anywhere.            | Have to be under sys.path (can be     |
|                                     | configured and expanded).             |
+-------------------------------------+---------------------------------------+
| Can easily execute a small piece of | We may have to keep a basic script    |
| Python code, not even in a file, eg | exec functionality next to the app    |
| ToolsMenu: Execute pyFormex command | framework                             |
+-------------------------------------+---------------------------------------+


Problems
--------

Here you can add any observations made concerning the execution of apps or
scripts.and especially differences between the two or functionality that you
would like to see changed.

Problems with known solution
............................

- Apps creating a dialog often use a global variable 'dialog' to store and
  access the dialog from different functions. Make sure that all functions
  that assign the dialog variable declare it to be global. 
  This needs to fixed mostly in the 'Run' functions, which contains the code
  previously not inside a function.

- Apps with syntax errors can not be loaded nor run. Exceptions raised
  during application load are filtered out by default. Setting the 
  configuration variable 'raiseapploadexc' to True will make such errors
  be shown.


Unsolved problems
.................

- Apps creating a permanent (non-blocking, modeless) dialog can currently
  not be rerun (reload and run). We could add such facility if we use
  a default attribute name, e.g. _dialog. Reloading would then close the
  dialog, and running would reopen it.



.. End

