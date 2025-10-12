# Quick Guide: Adding Movie Trailers

## 🎬 How to Add a Trailer to a Movie

### Step 1: Get YouTube URL
1. Go to YouTube
2. Find the movie trailer
3. Copy the URL from the address bar

**Example URL formats (all work):**
```
https://www.youtube.com/watch?v=TcMBFSGVi1c
https://youtu.be/TcMBFSGVi1c
https://www.youtube.com/embed/TcMBFSGVi1c
```

### Step 2: Add to Movie in Admin
1. Go to http://127.0.0.1:8000/admin/
2. Click "Movies"
3. Click on the movie you want to edit
4. Scroll to "Media" section
5. Paste YouTube URL in "Trailer url" field
6. Click "Save"

### Step 3: View on Website
1. Go to http://127.0.0.1:8000/movies/
2. Look for "Trailer Available" badge on the movie card
3. Click "Details" button
4. Watch the embedded trailer!

## 🎯 Where Trailers Appear

### Movie List Page (`/movies/`)
- Shows "Trailer Available" badge (red)
- "Details" button takes you to trailer

### Movie Detail Page (`/movies/<id>/`)
- Large embedded YouTube player
- Full movie information
- Available shows for booking

## 📝 Popular Movie Trailers for Testing

Copy and paste these URLs into your movies:

**Marvel Movies:**
```
Avengers Endgame: https://www.youtube.com/watch?v=TcMBFSGVi1c
Iron Man: https://www.youtube.com/watch?v=8ugaeA-nMTc
Black Panther: https://www.youtube.com/watch?v=xjDjIWPwcPU
```

**DC Movies:**
```
The Dark Knight: https://www.youtube.com/watch?v=EXeTwQWrcwY
Wonder Woman: https://www.youtube.com/watch?v=1Q8fG0TtVAY
Aquaman: https://www.youtube.com/watch?v=WDkg3h8PCVU
```

**Sci-Fi:**
```
Inception: https://www.youtube.com/watch?v=YoHD9XEInc0
Interstellar: https://www.youtube.com/watch?v=zSWdZVtXT7E
The Matrix: https://www.youtube.com/watch?v=vKQi3bBA1y8
```

**Action:**
```
John Wick: https://www.youtube.com/watch?v=C0BMx-qxsP4
Mission Impossible: https://www.youtube.com/watch?v=wb49-oV0F78
Fast & Furious: https://www.youtube.com/watch?v=aSiDu3Ywi8E
```

## ✅ Checklist

Before adding a trailer:
- [ ] Find movie on YouTube
- [ ] Copy the full URL
- [ ] Log into Django admin
- [ ] Navigate to Movies
- [ ] Find and edit the movie
- [ ] Paste URL in "Trailer url" field
- [ ] Save the movie
- [ ] Test on website

## 🎨 What Users See

**Without Trailer:**
- Movie card shows only basic info
- "Details" button still works (shows movie info only)

**With Trailer:**
- Red "Trailer Available" badge appears
- "Details" page includes embedded YouTube player
- Users can watch before booking

## 💡 Tips

1. **Use Official Trailers**: Always use official movie trailers from studios
2. **Test the URL**: Open the YouTube URL in a browser first to make sure it works
3. **Short URLs Work**: You can use youtu.be short links
4. **No Playlists**: Use individual video URLs, not playlists
5. **Quality**: Choose HD trailers for better user experience

## 🚀 Already Running?

The server auto-reloads when you:
- Add new trailer URLs in admin
- The changes appear immediately on the website
- No need to restart the server!

## 📱 Mobile Friendly

Trailers work great on:
- ✅ Desktop computers
- ✅ Tablets
- ✅ Mobile phones
- ✅ All modern browsers

---

**That's it!** Start adding trailers to make your movie booking site more engaging! 🎬🍿
