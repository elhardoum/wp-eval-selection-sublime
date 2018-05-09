# WP CLI eval code selection

This Sublime Text extension allows you to easily debug parts of your code with [`wp eval`](https://developer.wordpress.org/cli/commands/eval/) command while editing the code with Sublime Text.

Add a shortcut to run this tool while pressing a bunch of keys: 

```json
{ "keys": ["shift+ctrl+e"], "command": "wpclievalselection" }
```

This will execute the command when you press <kbd>shift</kbd>+<kbd>ctrl</kbd>+<kbd>c</kbd> combined. And of course you can set the letters of your choosing.

Here's an example output:

```

=======================

> Evaluating code

`echo get_bloginfo('name');`

> Response

wpdev

> Evaluated in

0.32 ms

=======================

> Evaluating code

`echo get_bloginfo('admin_email');`

> Response

somesecretemail@outlook.com

> Evaluated in

0.32 ms

=======================

> Evaluating code

`echo get_bloginfo('version');`

> Response

4.9.5

> Evaluated in

0.33 ms

```