Helical Boring G-Code Readme

FOR USE WITH PYTHON 2.7.3 
NEW VERSION WILL NOT WORK

To create multiple holes, enter centerpoints as follows
	
	Centerpoint X: X1,X2,X3
	Centerpoint Y: Y1,Y2,Y3
	Centerpoint Z: Z1,Z2,Z3
	

Any number of centerpoints may be entered, holes will be made at each location, each with the same parameters.
	Note: Each axis must have the same number of coordinates. 
	
		For Example,
		
		Centerpoint X: X1,X2,X3
		Centerpoint Y: Y1,Y2,Y3
		Centerpoint Z: Z1,Z2
		
		will produce an error.
		
G-Code Output follows the following pattern

	1. Call Tool #
	
	2. Turn spindle on clockwise at set speed (IF APPLICABLE)
	
	3. Turn on flood coolant (IF APPLICABLE)
	
	4 .Rapid to Z rapid height
	
	5. Rapid to X, Y start of first hole
	
		6. Feed at set feedrate to .005 over Z centerpoint
		
		7. Move to X, Y start of first cut
		
			8. Spiral plunge at set entry angle, with plunge radius not to exceed (.9 * Tool Diameter), to (Current Z location - set D.O.C.)
			
			9. Interpolate outwards at set W.O.C. roughing diameter 
			
			10. Return to 7. if not at full depth
			
		11. Interpolate to finishing diameter
		
		12. Rapid back to Z rapid height
		
		13. Return to 5. if more holes
		
		
			
			
		