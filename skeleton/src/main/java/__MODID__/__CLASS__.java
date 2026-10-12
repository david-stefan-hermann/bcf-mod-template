package __MODID__;

import bcf.guidebook.GuideBookItem;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

import java.util.function.Function;

public final class __CLASS__ implements ModInitializer {
    public static final String MOD_ID = "__MODID__";

    /** Everything the mod adds in one book; given once to every player. */
    public static final Item GUIDE_BOOK = item("guide_book", props -> new GuideBookItem(props.stacksTo(1), GuideBook.BOOK));

    public static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(MOD_ID, path);
    }

    @Override
    public void onInitialize() {
        Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, id("main"), FabricCreativeModeTab.builder()
                .icon(() -> new ItemStack(GUIDE_BOOK))
                .title(Component.translatable("itemGroup." + MOD_ID))
                .displayItems((params, out) -> out.accept(GUIDE_BOOK))
                .build());
        GuideBook.BOOK.giveOnJoin();
    }

    private static Item item(String name, Function<Item.Properties, Item> factory) {
        Identifier id = id(name);
        return Registry.register(BuiltInRegistries.ITEM, id, factory.apply(new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id))));
    }
}
