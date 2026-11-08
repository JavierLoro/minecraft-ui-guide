import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import com.google.gson.*;
import com.mojang.serialization.JsonOps;
import net.minecraft.SharedConstants;
import net.minecraft.server.Bootstrap;
import net.minecraft.data.registries.VanillaRegistries;
import net.minecraft.resources.RegistryOps;
import net.minecraft.commands.*;
import net.minecraft.server.permissions.PermissionSet;
import net.minecraft.world.flag.FeatureFlags;
import net.minecraft.server.dialog.Dialog;
public class ValidateData {
 public static void main(String[] args) throws Exception {
  SharedConstants.tryDetectVersion();Bootstrap.bootStrap();
  var lookup=VanillaRegistries.createReloadableLookup(VanillaRegistries.createWorldLookup());
  var ops=RegistryOps.create(JsonOps.INSTANCE,lookup);
  var commands=new Commands(Commands.CommandSelection.ALL,CommandBuildContext.simple(lookup,FeatureFlags.DEFAULT_FLAGS));
  var source=Commands.createCompilationContext(PermissionSet.ALL_PERMISSIONS);
  var fixtures=new HashMap<String,String>();
  for(var key:List.of("id","pieces","coins","hud","anchor","primary","toggle","settings","close"))fixtures.put(key,"1");
  fixtures.put("goal","5");fixtures.put("who","#validate");fixtures.put("primary_label","Fabricar pieza");
  fixtures.put("toggle_label","Ocultar HUD");fixtures.put("white","#ffffff");fixtures.put("teal","#51d4cb");
  fixtures.put("bar","\uE012");fixtures.put("back","\uF011\uF013\uF014\uF015");
  int count=0,dialogs=0,errors=0;
  try(var paths=Files.walk(Path.of(args[0]))) {
   for(Path path:paths.filter(Files::isRegularFile).toList()) {
    if(path.toString().endsWith(".mcfunction")) {
     int lineNo=0;
     for(String line:Files.readAllLines(path)) {
      lineNo++;line=line.strip();if(line.isEmpty()||line.startsWith("#"))continue;
      if(line.startsWith("$")) {
       line=line.substring(1);var match=Pattern.compile("\\$\\((\\w+)\\)").matcher(line);var expanded=new StringBuffer();
       while(match.find()) {
        String value=fixtures.get(match.group(1));if(value==null)throw new IllegalStateException("Missing fixture "+match.group(1));
        match.appendReplacement(expanded,Matcher.quoteReplacement(value));
       }
       match.appendTail(expanded);line=expanded.toString();
      }
      if(line.startsWith("dialog show @s taller:settings/")) {
       String name=line.substring("dialog show @s taller:settings/".length());
       line="dialog show @s "+JsonParser.parseString(Files.readString(Path.of(args[0],"data/taller/dialog/settings/"+name+".json"))).toString();
      }
      try {Commands.validateParseResults(commands.getDispatcher().parse(line,source));count++;}
      catch(Exception error) {System.out.println("INVALID "+path.getFileName()+":"+lineNo+" "+error.getMessage());errors++;}
     }
    } else if(path.toString().endsWith(".json")&&path.toString().contains("dialog")&&!path.toString().contains("tags")) {
     var result=Dialog.DIRECT_CODEC.parse(ops,JsonParser.parseString(Files.readString(path)));
     if(result.error().isPresent()) {System.out.println("INVALID DIALOG "+path+" "+result.error().get().message());errors++;}
     else dialogs++;
    }
   }
  }
  System.out.println("NATIVE VALIDATION: commands="+count+" dialogs="+dialogs+" errors="+errors);
  if(errors>0)System.exit(1);
 }
}