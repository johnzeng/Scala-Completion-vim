import java.util.spi
import java.util.prefs

class MyTest{
  def hello() = "hello"
  def getNohello() = "hello"
  def newget() = "new"
  var hi = "123"
  hi
}

object Test {
  val five = 5
  val hello = new MyTest()
  val amount = five / 1
  amount * 8
  hello.getNohello
  hello.hello
  hello.newget
  
  
}


