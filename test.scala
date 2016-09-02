import java.util

class MyTest{
  def hello() = "hello"
  def getNohello() = "hello"
  def newget() = "new"
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

