# Scala-Completion-vim
Still very buggy scala vim completion plugin based on [Scala-completion-base](https://github.com/johnzeng/Scala-completion-Base)

Client-Server Arch completion plugin. It's not working fine now because it will spend lots of time to wait until the compile is finished.

# screen cast
![testing](https://github.com/johnzeng/Images/blob/master/scala-complete-vim/V1.gif)

# Currently supported feature
- completion for symbol(even those from implicit conversions)
- completion for import

# need to be supported
- third party jar lib including.
- (maybe) sbt support.
- ~~(maybe) CS architecture to boost the plugin.~~

# known limit
- Can not do completion if the file is not compilable. So `import java` is not going to give any completion because this will throw an exception when you do compile 

