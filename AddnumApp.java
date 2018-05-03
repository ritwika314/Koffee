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
   private MutualExclusion mutex0;
   private boolean wait0 = false;
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
      mutex0 = new GroupSetMutex(gvh,0);
      
   }
   @Override
   public List<Object> callStarL()  {
   
      dsm.createMW("sum",0);
      dsm.createMW("numadded",0);
      while(true)  {
      
         sleep(100);
         //adding
         if (!(added)) {
         
            if(!wait0) {
            
               mutex0.requestEntry(0);
               wait0 = true;
               
            }
            if (mutex0.clearToEnter(0))  {
            
               if (dsm.get("sum","*") == null) {continue;}
               sum = Integer.parseInt(dsm.get("sum","*"));
               sum = (sum + (pid * 2));
               dsm.put("sum","*",sum);
               if (dsm.get("numadded","*") == null) {continue;}
               numadded = Integer.parseInt(dsm.get("numadded","*"));
               numadded = (numadded + 1);
               dsm.put("numadded","*",numadded);
               added = true;
               mutex0.exit(0);
               
            }
            continue;
            
         }
         //finalsum
         if (dsm.get("numadded","*") == null) {continue;};
         numadded = Integer.parseInt(dsm.get("numadded","*"));
         if ((numadded == numBots)) {
         
            if (dsm.get("sum","*") == null) {continue;}
            sum = Integer.parseInt(dsm.get("sum","*"));
            finalsum = sum;
            continue;
            
         }
         
      }
      
   }
   
   
}
