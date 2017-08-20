# Troubleshooting

['python' is not recognized as an internal or external command, operable program or batch file](#notPath)

## 'python' is not recognized as an internal or external command, operable program or batch file <a id = "notPath">

1. Press `Win` + `R`.

1. Write `control panel` then press `Enter`. <br>![exammple](http://i.imgur.com/5q1U9X9.png)

1. Click on `System and Security`. <br>![example](http://i.imgur.com/bLwPXUu.png)

1. Click on `System`. <br>![example](http://i.imgur.com/d3vOdVH.png)

1. Click on `Advanced system settings`. <br>![example](http://i.imgur.com/zbBFieZ.png)

1. Click on `Environment Variables...`.  <br>![example](http://i.imgur.com/REi67pX.png)

1. Click on the `PATH` line and click `Edit`. ![example](http://i.imgur.com/6WbJWTr.png)

1. If you're on Windows 7 or older versions, add `;C:\Users\YOUR_USER_NAME_HERE\AppData\Local\Programs\Python\Python36-32` to the `Variable's value` textbox. ![example](http://i.imgur.com/1IZCqlz.png)<br> If you're on Windows 10, click on `New`, then name the new line `C:\Users\YOUR_USER_NAME_HERE\AppData\Local\Programs\Python\Python36-32` ![example](http://i.imgur.com/vBFZmRh.png)

1. Restart the command prompt.