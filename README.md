# logx: best practice python logging with zero config

Configuring logging is tedious. Reading the logging module docs makes me tired.

Wouldn't it be nice to log as easily as doing a print statement, without any upfront config?

## Obligatory example

Enter `logx`. It's as simple as:

    >>> from logx import log
    >>> log.info('hello world')
    hello world
    >>> log.set_default_format()
    >>> log.warn('warning!')
    [2018-02-26 21:51:16,971] WARNING [__main__.<module>:1] warning!

Logs get logged automatically to the logger whose name matches the current module.

## List of sweet features

- Creates loggers lazily/as needed/on demand and **logs to the appropriate logger automatically**. If you're in the "acme" module it'll log to a log called "acme", no need worry about logger names and instances.
- **Shows all log messages by default**, which follows the principle of least surprise and is probably what you want when debugging.
- Included default handler **logs to the appropriate standard output stream by default**: Errors and warnings to stderr, the rest to stdout.
- Allows easy following of best practice when including log statements in a library: **Just call log.create_null_handler() in your module.**
- **Uses the standard logging library**, so you can still customize your setup as much as you want/need. Plays nicely with your existing logging config files.
- **Includes the very useful logging_tree module** for viewing your current logging configuration. `logx.print_diagram()`

## Install

    >>> pip install logx

## Contribute

Issues and pull requests welcome, hit me. Am I doing logging completely wrong? Critique welcome, even if very pedantic.
