package __MODID__;

import bcf.guidebook.Book;
import bcf.guidebook.BookTheme;
import bcf.guidebook.Chapter;
import bcf.guidebook.Section.Heading;
import bcf.guidebook.Section.ItemLine;
import bcf.guidebook.Section.Quote;
import bcf.guidebook.Section.Text;
import net.minecraft.world.item.ItemStack;

import java.util.List;

/**
 * The content of the guide book, as data: chapters of sections, which the screen of bcf-guide-book-lib wraps and
 * breaks into pages. Texts are translation keys {@code __MODID__.book.<key>} in the language files. What goes into
 * which chapter is in STANDARDS.md of bcf-mod-template.
 */
public final class GuideBook {
    /** The library's plain slate grey; give the mod its own colours with the builder's methods. */
    public static final Book BOOK = Book.of(__CLASS__.MOD_ID, BookTheme.builder().build(), GuideBook::chapters);

    private GuideBook() {
    }

    public static String key(String name) {
        return BOOK.key(name);
    }

    /** Built when the book opens: item stacks need the registries. */
    public static List<Chapter> chapters() {
        return List.of(
                new Chapter(key("start"), new ItemStack(__CLASS__.GUIDE_BOOK), Chapter.Side.RIGHT, List.of(
                        new Text(key("start.text")), new Quote(key("start.motto")),
                        new Heading(key("heading.steps")),
                        new ItemLine(List.of(new ItemStack(__CLASS__.GUIDE_BOOK)), key("start.step1")),
                        new Heading(key("heading.crafting")), BOOK.recipe("guide_book"),
                        new Text(key("start.recipe")))));
    }
}
