import csv
import math
import matplotlib.pyplot as plt
"""
input two integers rNIR,rRed
output calculated NDVI value round to 3 d.p.
"""
def calculateNDVI(rNIR, rRed):
    denominator = rNIR + rRed
    if (denominator == 0):
        return "INF"
    NDVI = (rNIR - rRed) / denominator
    return round(NDVI, 3)
"""
input one integer n
"""
def displayNbyNNDVI(n):
    #in order to define a function
    with open('./data/band_NIR.csv') as csvNIR:
        with open('./data/band_red.csv') as csvRed:
            readerNIR = csv.reader(csvNIR, delimiter=',')
            readerRed= csv.reader(csvRed, delimiter=',')
            a = 0
            #loop each row of data files
            for rowNIR, rowRed in zip(readerNIR, readerRed):
                #when loop in to nth row ,stop run
                if (a == n+1):
                    break
                #each loop a plus one
                if (a == 0):
                    a += 1
                    continue
                a += 1
                b = 0
                rowNDVI = []
                # in order to show each item
                for rNIR, rRed in zip(rowNIR, rowRed):
                    #  stop at nth loop
                    if (b == n+1):
                        break
                    # each loop b plus one
                    if (b == 0):
                        b += 1
                        continue
                    b += 1
                    # in order to avoid to appear the empty space
                    if (rNIR == ''):
                        continue
                    # in order to avoid to appear the empty space
                    if (rRed == ''):
                        continue
                    rNIR = float(rNIR)
                    rRed = float(rRed)
                    rowNDVI.append(calculateNDVI(rNIR,rRed))
                print(rowNDVI)
"""
output the number of each category
"""
def countCategory ():
    with open('./data/band_NIR.csv') as csvNIR:
        with open('./data/band_red.csv') as csvRed:
            readerNIR = csv.reader(csvNIR, delimiter=',')
            readerRed= csv.reader(csvRed, delimiter=',')
            count_non_vegetatedCategory=0
            count_low_vegetatedCategory=0
            count_medium_vegetatedCategory=0
            count_high_vegetatedCategory = 0
            count_very_high_vegetatedCategory = 0
            a = 0
            #loop each row of data files
            for rowNIR, rowRed in zip(readerNIR, readerRed):
                # stop at nth row
                if (a == 0):
                    a += 1
                    continue
                a += 1
                b = 0
                # loop each row of data files
                for rNIR, rRed in zip(rowNIR, rowRed):
                    if (b == 0):
                        b += 1
                        continue
                    b += 1
                    # clean the empty space in rNIR
                    if (rNIR == ''):
                        continue
                    # clean the empty space in rRed
                    if (rRed == ''):
                        continue
                    rNIR = float(rNIR)
                    rRed = float(rRed)
                    t=calculateNDVI(rNIR,rRed)
                    #according to different NDVI range to making a count
                    if t < 0:
                        count_non_vegetatedCategory+=1
                    elif t < 0.3:
                        count_low_vegetatedCategory+=1
                    elif t < 0.6:
                        count_medium_vegetatedCategory+=1
                    elif t <0.9:
                        count_high_vegetatedCategory+=1
                    else:
                        count_very_high_vegetatedCategory+=1
            print("count_non_vegetatedCategory",count_non_vegetatedCategory)
            print("count_low_vegetatedCategory",count_low_vegetatedCategory)
            print("count_medium_vegetatedCategory",count_medium_vegetatedCategory)
            print("count_high_vegetatedCategory",count_high_vegetatedCategory)
            print("count_very_high_vegetatedCategory",count_very_high_vegetatedCategory)
"""
input one SWP 
Out put NDVI 
"""
def calculatepredictedNDVI(SWP) :
    NDVI= 0.26 * SWP+ 0.96
    return round (NDVI,3)
"""
input two lists SWPs and positions indicating the 2019 SWP valud of each position
positions = [(605, 1100), (3712, 500), (2124,1072), (196,85 ), (4100,2241)]
SWPs = [-2.196, -2.511, -2.261, -3.964, -3.078]
"""
def calculateRMSE(positions, SWPs):
    with open('./data/band_NIR.csv') as csvNIR:
        with open('./data/band_red.csv') as csvRed:
            readerNIR = list(csv.reader(csvNIR, delimiter=','))
            readerRed = list(csv.reader(csvRed, delimiter=','))
            sum_of_square_difference = 0
            #In order to calculate the sum of squre differences of each item
            for position, swp in zip(positions, SWPs):
                x,y=position
                rNIR = readerNIR[x+1][y+1]
                rRed = readerRed[x+1][y+1]
                rNIR = float(rNIR)
                rRed = float(rRed)
                aNDVI = calculateNDVI(rNIR, rRed)
                pNDVI = calculatepredictedNDVI(swp)
                sum_of_square_difference += (pNDVI - aNDVI)**2
            rmse = math.sqrt(sum_of_square_difference/len(positions))
    return round(rmse,3)
"""
input list of SWP values
output list of predicted NDVI values
"""
def calculatePredictedNDVIs(SWPs):
    NDVI_p = []
    for SWP in SWPs:
        NDVI_p.append(calculatepredictedNDVI(SWP))
    return NDVI_p
def drawNDVIGraph():
    years=[2019,2020,2021,2022]
    swps_1=[-2.196,-1.974,-1.82,-1.722]
    swps_2=[-2.511,-2.169,-2.01,-1.63]
    swps_3=[-2.261, -2.154, -1.929, -1.649]
    swps_4=[-3.964, -3.399, -2.745, -2.648]
    swps_5=[-3.078, -2.473, -2.423, -2.129]
    NDVI_P1 = calculatePredictedNDVIs(swps_1)
    NDVI_P2 = calculatePredictedNDVIs(swps_2)
    NDVI_P3 = calculatePredictedNDVIs(swps_3)
    NDVI_P4 = calculatePredictedNDVIs(swps_4)
    NDVI_P5 = calculatePredictedNDVIs(swps_5)
    plt.plot(years,NDVI_P1,label="NDVI for (605, 1100)")
    plt.plot(years,NDVI_P2,label="NDVI for (3712, 500)")
    plt.plot(years, NDVI_P3, label="NDVI for (2124, 1072)")
    plt.plot(years, NDVI_P4, label="NDVI for (196, 85) ")
    plt.plot(years, NDVI_P5, label="NDVI for (4100, 2241)")
    plt.legend()
    plt.savefig("ex1_question5.png", format="png")
    plt.show()



if __name__ == "__main__":
    positions = [(1100, 605), (500, 3712), (1072, 2124), (85, 196), (2241, 4100)]
    SWPs = [-2.196, -2.511, -2.261, -3.964, -3.078]

    # Q 1
    displayNbyNNDVI(5)
    # Q 2
    countCategory()
    # Q 3
    print(calculatePredictedNDVIs(SWPs))
    # Q 4
    print(calculateRMSE(positions, SWPs))
    # Q 5
    drawNDVIGraph()

