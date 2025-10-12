# How to Add Trailers - Step by Step

## The trailer section won't appear until you add a YouTube URL!

### Quick Steps:

1. **Open Admin Panel**
   - Go to: http://127.0.0.1:8000/admin/
   - Login with your admin credentials

2. **Navigate to Movies**
   - Click on "Movies" in the left sidebar

3. **Edit a Movie**
   - Click on any movie name (e.g., "avengers")

4. **Add Trailer URL**
   - Scroll down to the "Media" section
   - Find the "Trailer url" field
   - Paste a YouTube URL, for example:
   ```
   https://www.youtube.com/watch?v=TcMBFSGVi1c
   ```

5. **Save**
   - Click "Save" button at the bottom

6. **View the Movie**
   - Go to: http://127.0.0.1:8000/movies/
   - Click "Details" button on the movie
   - You should now see the trailer!

## Example YouTube URLs to Test:

**Avengers Endgame:**
```
https://www.youtube.com/watch?v=TcMBFSGVi1c
```

**Iron Man:**
```
https://www.youtube.com/watch?v=8ugaeA-nMTc
```

**The Dark Knight:**
```
https://www.youtube.com/watch?v=EXeTwQWrcwY
```

**Inception:**
```
https://www.youtube.com/watch?v=YoHD9XEInc0
```

## Why Can't You See the Trailer?

The movie detail page template has this logic:

```django
{% if movie.get_youtube_embed_url %}
    <!-- Trailer section shows here -->
{% endif %}
```

This means:
- ❌ No trailer URL = No trailer section displayed
- ✅ Trailer URL added = Trailer section appears with video player

## What You'll See After Adding Trailer:

**Before (No Trailer URL):**
- Movie detail page shows: Poster, Info, Description, Available Shows
- NO video player section

**After (With Trailer URL):**
- Movie detail page shows: Poster, **Trailer Player**, Info, Description, Available Shows
- Red "Watch Trailer" card with embedded YouTube video

## Screenshot of What to Look For in Admin:

When editing a movie, scroll down to find:

```
┌─ Media ────────────────────────────────────┐
│                                             │
│  Trailer url:                               │
│  ┌──────────────────────────────────────┐  │
│  │  Paste YouTube URL here              │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ℹ️ Add YouTube trailer URL                 │
│  (e.g., https://www.youtube.com/watch?v=...) │
│                                             │
└─────────────────────────────────────────────┘
```

## Troubleshooting:

**Still can't see trailer after adding URL?**

1. Make sure you clicked "Save" after adding the URL
2. Refresh the movie detail page (Ctrl+F5)
3. Check the URL format is correct (YouTube URL)
4. Look in the browser console for errors (F12)

**Need help?**
- The trailer field is optional
- You need to add it manually for each movie
- Only YouTube URLs are supported currently

---

**Ready to add your first trailer? Go to the admin panel now!** 🎬
