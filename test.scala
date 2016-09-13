import java.util.spi.TimeZoneNameProvider
import java.util.prefs
import com.auth0.jwt._
import java.util.HashMap

class MyTest{
  def hello() = "hello"
  def getNohello() = "hello"
  def newget() = "new"
  var hi = "123"
  
  hi.contains("123")
  
}

object Test {
  val five = 5
  val hello = new MyTest()
  val amount = five / 1
  amount * 8
  hello.getNohello
  hello.hello
  hello.newget
  val b = Seq(1,1)
  val c = b.map(a => a+1)

  val issuer = "https://mydomain.com/"
  val secret = "ababa"

  val iat = System.currentTimeMillis() / 1000l // issued at claim 
  val exp = iat + 60l // expires claim. In this case the token expires in 60 seconds

  val signer = new JWTSigner(secret)
  val claims = new HashMap[String, Object]()
  claims.put("iss", issuer)
//  claims.put("exp", exp)
//  claims.put("iat", iat)

  val jwt = signer.sign(claims)
 
}
