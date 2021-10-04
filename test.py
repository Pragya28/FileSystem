from keys import getMyPrivateKey, getSharedKey

a_passkey = "Qmw79xVfeKLO4SKgl8EA8Q==$evZGcZy9xcZQQmYXAPBA0A=="
q_passkey = "rhHr4f582zI0WlLEYKvKBg==$8y3J/AVtwRLRldpwDuboOA=="

a_public = "81531658638336074795314620494541552772439803116097948805626689221397147048722$27860180888316394257284358073505279410233815754493096047264227948270463534489"
q_public = "98350749256686834271254013723185769569928953404582747351674432971642814561892$89136156804694674092660661439726259321423351620066232812599288861302587713139"

a_secret = "kfzSgwk0pTmCWvIr0yxv48uyL+fgOFNasVnkIEVf/rEjb6uoav6bU4uVzMaQ7fF1TsYQqAp9v0q/jeyaTrhVIAfl5IQZAJGzI5vgHLIJdLs=$Kl8hB0yoz75UJg8VsK+vbg=="
q_secret = "xB/s3HlfilSyz/y/aWDdaxmDxQk1qoOf1aMw6pAo90UrGgfhXE08TnLrR+YEIR7iN0nzngLs1W6eFwOnKpMpqfGpVslFFZur0KM73mv3jVA=$oXIHlmNlk1rmjeyuBbsi3w=="

a_private = getMyPrivateKey(a_passkey, a_secret)
q_private = getMyPrivateKey(q_passkey, q_secret)

a_shared = getSharedKey(a_public, q_private)
q_shared = getSharedKey(q_public, a_private)

print(a_shared == q_shared)