package addnum;


import edu.illinois.mitra.cyphyhousefunctions.DSMMultipleAttr;
import edu.illinois.mitra.cyphyhouseinterfaces.DSM;
import edu.illinois.mitra.cyphyhouseinterfaces.MutualExclusion;
import edu.illinois.mitra.cyphyhousefunctions.GroupSetMutex;

import java.net.*;
import java.io.*;
import java.util.*;
import java.lang.*;
import java.nio.file.*;
import java.util.stream.Stream;

import edu.illinois.mitra.cyphyhousegvh.GlobalVarHolder;
import edu.illinois.mitra.cyphyhouseinterfaces.LogicThread;

public class AddnumApp extends LogicThread  {

   private static final String TAG = "AddnumApp";
   private DSM dsm;
   private int numBots;
   private int pid;
   
   
   int sum = 0;
   int numadded = 0;
   boolean added = false;
   int finalsum;
   
   public Addnum(GlobalVarHolder gvh)  {
   
      super(gvh);
      String intValue = name.replaceAll("[^0-9]", "");
      pid = Integer.parseInt(intValue);
      numBots = gvh.id.getParticipants().size();
      dsm = new DSMMultipleAttr(gvh);
      
   }
   @Override
   public List<Object> callStarL()  {
   
      while(true)  {
      
         if (!(added)) {
         
            sum = (sum + (pid * 2));
            numadded = (numadded + 1);
            added = true;
            continue;
            
         }
         if ((numadded == numBots)) {
         
            finalsum = sum;
            continue;
            
         }
         
      }
      
   }
   
   
}
