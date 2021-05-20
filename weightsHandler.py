import weights
import os
import ast


class WeightsHandler(object):
    def __init__(self, file_name):
        self.file_name = file_name

        if os.path.getsize(self.file_name):
            self.read_weights = open(self.file_name, "r")
            line_1 = ast.literal_eval(
                self.read_weights.readline().split("=")[1][1:-1])
            line_2 = ast.literal_eval(
                self.read_weights.readline().split("=")[1][1:])
            line_3 = ast.literal_eval(
                self.read_weights.readline().split("=")[1][1:])

            weights.initPosPnts = [[int(i) for i in j] for j in line_1]
            weights.finalPosPnts = [[int(i) for i in j] for j in line_2]
            weights.game = line_3
        else:
            weights.initPosPnts = [
                [0 for i in range(0, 64)] for j in range(0, 6)]
            weights.finalPosPnts = [
                [0 for i in range(0, 64)] for j in range(0, 6)]
            weights.game = 0

        self.write_weights = open(self.file_name, "w")
        self.writeWeightsToFile()

    def writeWeightsToFile(self):
        self.write_weights.seek(0, 0)
        self.write_weights.write(
            "initPosPnts = {}\nfinalPosPnts = {}\ngame = {}".format(
                str(weights.initPosPnts), str(weights.finalPosPnts), str(weights.game))
        )
        # self.write_weights.write(
        #     "initPosPnts = {}\nfinalPosPnts = {}".format(
        #         str(weights.initPosPnts),
        #         str(weights.finalPosPnts)
        #     )
        # )

    def closeWeightsFile(self):
        self.write_weights.close()

    def setWeights(self, initPosWeights, finalPosWeights):
        weights.initPosPnts = initPosWeights[:]
        weights.finalPosPnts = finalPosWeights[:]

    def setGameNum(self, game):
        weights.game = game + 1

    def getWeights(self):
        return (weights.initPosPnts[:], weights.finalPosPnts[:])

    def getGameNum(self):
        return weights.game
