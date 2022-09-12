###Renderer will read polygons and lines created and translate them to 3D using a funny little recursive loop running 15 times every second. How cute!
print("Loading Framework...")
sleep(.5)
renderPoly1 = Polygon(
	333, 56,
	313, 48,
	239, 73,
	177, 62,
	154, 72,
	140, 159,
	155, 231,
	197, 302,
	215, 316,
	238, 321,
	272, 312,
	306, 290,
	320, 268,
	333, 207,
	347, 154,
	350, 129,
	fill = "white", border = "black", borderWidth = 1
)
sleep(.5)
renderPoly2 = Polygon(
	117, 74,
	116, -3,
	377, -3,
	381, 77,
	347, 154,
	333, 56,
	313, 48,
	239, 73,
	177, 62,
	154, 72,
	140, 159,
	fill = "white", border = "black", borderWidth = 1
)
sleep(.15)
renderLine1 = Line(
	220, 180,
	214, 209
)
sleep(.15)
renderLine2 = Line(
	214, 209,
	216, 216
)
sleep(.15)
renderLine3 = Line(
	216, 216,
	229, 220
)
sleep(.15)
renderLine4 = Line(
	229, 220,
	242, 218
)

app.setMaxShapeCount(900)
Sound("https://python-rickroll.s3.us-west-2.amazonaws.com/Never/audio.mp3").play()
for i in range(1,848):
	Image("https://python-rickroll.s3.us-west-2.amazonaws.com/Never/Rick"+str(i*5).rjust(4, "0")+".jpg", 0, 0)
	sleep(.25)