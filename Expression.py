
#LDTP code genereation is done here


import numpy as np
import cv2
import matplotlib.pyplot as plt

#finding Primary Direction

def findMax(a,b,c,d):
  primaryDirection=-1
  maxi=max([a,b,c,d],key=abs)
  if maxi==a:
    primaryDirection=0
  elif maxi==b:
    primaryDirection=1
  elif maxi==c:
    primaryDirection=2
  else:
    primaryDirection=3

  return primaryDirection,maxi

# finding Secondary Direction

def findSecondMax(a,b,c,d):
  secondaryDirection=-1
  l=[a,b,c,d]
  maxi=max(l,key=abs)
  l.remove(maxi)
  maxi=max(l,key=abs)
  if maxi==a:
    secondaryDirection=0
  elif maxi==b:
    secondaryDirection=1
  elif maxi==c:
    secondaryDirection=2
  else:
    secondaryDirection=3
  
  return secondaryDirection,maxi

# finding Ternary Pattern

def findTernary(value,sigma):
  if value<-sigma:
    return 2
  elif value>sigma:
    return 1
  elif -sigma<=value and value<=sigma:
    return 0
  else:
    pass
# finding ldtp codes

def findLDTP(d1,d2,t1,t2):
  res=0
  res+=(2**6)*d1
  res+=(2**4)*t1
  res+=(2**2)*d2
  res+=t2
  return res

#function to find the thresold value

def findSigma(matrix):
  matrix.sort()
  #print(matrix)
  return sum(matrix)//len(matrix)



def findEmotion(image):
#Masks M-0 to M-3 
  M=[
    [
      [-1,0,1],
      [-2,0,2],
      [-1,0,1]],
    [
      [0,1,2],
      [-1,0,1],
      [-2,-1,0]],
    [
      [1,2,1],
      [0,0,0],
      [-1,-2,-1] ],
    [
      [2,1,0],
      [1,0,-1],
      [0,-1,-2]
    ]
  ]
  temp=[[0,0,0],[0,0,0],[0,0,0]]

  r,c= image.shape
  LDTP = np.zeros((r-2,c-2))

  #intialize all the lists to empty

  matrix1=[]
  matrix2=[]
  matrix3=[]
  matrix4=[]

  print(LDTP)
  print()

  for i in range(r-2):
    for j in range(c-2):
      for k in range(3):
        for l in range(3):
          temp[k][l]=image[i+k][j+l]
          
      #convolution with first mask
      res1=0
      s=M[0]
      for k in range(3):
        for l in range(3):
          matrix1.append(s[k][l]*temp[k][l])
          res1+=s[k][l]*temp[k][l]

      
      #convolution with second mask
      res2=0
      s=M[1]
      for k in range(3):
        for l in range(3):
          matrix2.append(s[k][l]*temp[k][l])
          res2+=s[k][l]*temp[k][l] 
     
      #convolution with third mask
      res3=0
      s=M[2]
      for k in range(3):
        for l in range(3):
          matrix3.append(s[k][l]*temp[k][l])
          res3+=s[k][l]*temp[k][l]
      
      #convolution with fourth mask
      res4=0
      s=M[3]
      for k in range(3):
        for l in range(3):
          matrix4.append(s[k][l]*temp[k][l])
          res4+=s[k][l]*temp[k][l]
      
      primaryDirection,maximumValue=findMax(res1,res2,res3,res4)

      secondaryDirection,secondMax=findSecondMax(res1,res2,res3,res4)

      if primaryDirection==0:
        
        sigma=findSigma(matrix1)
      elif primaryDirection==1:
        
        sigma=findSigma(matrix2)
      elif primaryDirection==2:
        
        sigma=findSigma(matrix3)
      elif primaryDirection==3:
      
        sigma=findSigma(matrix4)

      if secondaryDirection==0:
        sigma1=findSigma(matrix1)
      elif secondaryDirection==1:
        sigma1=findSigma(matrix2)
      elif secondaryDirection==2:
        sigma1=findSigma(matrix3)
      elif secondaryDirection==3:
        sigma1=findSigma(matrix4)

     
      primaryTernary=findTernary(maximumValue,sigma)

      secondaryTernary=findTernary(secondMax,sigma1)

      LDTP[i][j]=findLDTP(primaryDirection,secondaryDirection,primaryTernary,secondaryTernary)

      matrix1=[]
      matrix2=[]
      matrix3=[]
      matrix4=[]


  #printing the resultant LDTP for the iamge
  print(LDTP)
  #converting the LDTP to histograms
  plt.hist(LDTP.ravel(),256,[0,256])
  print("The histogram generated based on the ldtp codes is")
  print()
  plt.show()

image = cv2.imread("sad.png",0)
findEmotion(image)
