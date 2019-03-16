import aiml


class im:
    def get_alice(self):
        # Create the kernel and learn AIML files
        path = '/root/MHKG/Django/toolkit/aiml/std-startup.xml'
        kernel = aiml.Kernel()
        kernel.learn(path)
        kernel.respond("load aiml")
        return kernel

    # def getMsg(self, send):
    #     alice = self.get_alice()
    #     im = alice.respond(send)
    #     return im


# t = im()
# a = t.get_alice()
# while True:
#     print(a.respond(input(">>>")))
