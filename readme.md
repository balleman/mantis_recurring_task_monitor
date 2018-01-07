mantis_recurring_task_monitor
=============================

Summary
-------

This is a utility to support recurring tasks in MantisBT (https://www.mantisbt.org/).  


Concept of Operations
---------------------

A project is created that contains the issue masters for recurring tasks.  These
master issues provide custom fields to define the project into which instances
of the recurring tasks will be created, how often the task is to recur, and how
often an instance is to be updated with a reminder.  The python script is run
on a recurring basis (e.g., through cron) to poll the current and former instances
and add new issues or notes as needed.

Requirements
------------

MantisBT, patched to support adding relationships via the REST API.  This PR was
submitted to add that ability: https://github.com/mantisbt/mantisbt/pull/1265

Custom relationships are used to track the link between instance issues and their
master issue.  The config directory contains the definition for these relationships
that can be integrated into your Mantis configuration.

The master issues require the followign custom fields:

 * "Recur Days" - the number of days to wait since the last closed instance before 
creating a new instance
 * "Remind Days" - the number of days since the last update of an open instance
before adding a note reminding of the instance
 * "Instance Project" - the project into which new instances are created


