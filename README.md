# netzbeweis

This is a Proof-Of-Concept showing how to create fake evidence with [netzbeweis.de](https://netbeweis.de). Netzbeweis
takes screenshots of websites and signs them with the current date and time. This way they can be used as evidence for
legal purposes.

The problem is that it seems like you can just submit random images to their API and they will sign them anyway. It only
takes a bit of reverse-engineering of their browser extension.

I couldn't verify that this actually works, because I don't want to pay 10€ for their service just to test it. But based
on the successful API responses and their claim that the process is automated I'm pretty confident that it does actually
work.

This is a Proof-Of-Concept, I'm not advocating for using this for any real purposes.

## Authorization

The API requires a JWT token for authorization. To obtain one you need to have to pay them or signin with one of the
third-party platforms. To test it I have signed in with a fake email (it's not validated) with "XPERT". It's enough to
make the requests but I can't actually see the generated evidence because I don't actually have an XPERT account. My
test token is hardcoded into the script and should be valid until March 2023.

## Example Usage

Let's say you have this image of a clown saved as `clown.png`:
![](clown.png)

You now want evidence that this clown face is visible on my twitter profile (https://twitter.com/merlin_fuchs):

```shell
python3 -m pip install -r requirements.txt
python3 submit.py https://twitter.com/merlin_fuchs clown.png
```

This is all it takes! if you have replaced the hardcoded API token with one with a valid subscription you should receive
the "evidence".
