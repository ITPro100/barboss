# 🇺🇦 BARBOSS SHOP - Deployment Guide

## ✅ Поточний статус

### GitHub Repository
- **URL**: https://github.com/ITPro100/barboss
- **Статус**: ✅ Оновлено з українським контентом
- **Остання версія**: Повна локалізація для Barboss Room Ukraine

### Live Preview
- **Test Server**: https://8080-i8gykmywmluvo4pcnnaaz-6532622b.e2b.dev
- **Статус**: ✅ Працює

## 🏬 Що оновлено

### Український контент:
- ✅ Реальні товари з Telegram каналу
- ✅ Ціни в гривнях (UAH)
- ✅ Адреса: Київ, вул. Шота Руставели 27Б
- ✅ Контакти: @barbos_shop, @Barbooss_bot
- ✅ Instagram: @barbos_room, @barbos_room_reserve, @barbos_delivery
- ✅ Повідомлення "❌ NOT SHIP TO russia 🇷🇺"
- ✅ Слоган: "Всім мирного неба над головою, бережіть себе 🫡"

### Функціонал:
- ✅ Індикатор проданих товарів (SOLD)
- ✅ "Ціна по запросу" для деяких товарів
- ✅ Інтеграція з Telegram для замовлень
- ✅ Звернення до аудиторії як "квадратура"

## 📦 Деплой на Cloudflare Pages

### Варіант 1: Через GitHub (Рекомендовано)

1. **Перейдіть в Cloudflare Dashboard**
   - https://dash.cloudflare.com/
   - Увійдіть в акаунт

2. **Створіть Pages проект**
   - Workers & Pages → Create application → Pages
   - Connect to Git → GitHub
   - Виберіть репозиторій: `ITPro100/barboss`

3. **Налаштування**
   - Project name: `barboss-ukraine`
   - Production branch: `main`
   - Build command: *(залишити пустим)*
   - Build output directory: `/`

4. **Deploy**
   - Сайт буде доступний: https://barboss-ukraine.pages.dev

### Варіант 2: Пряме завантаження

1. Перейдіть на https://pages.cloudflare.com/
2. Direct Upload
3. Завантажте всі файли
4. Назва проекту: `barboss-ukraine`

## 🌐 Альтернативні платформи

### Netlify
```bash
# Перейдіть на https://app.netlify.com/drop
# Перетягніть всі файли
# Отримаєте миттєвий URL
```

### Vercel
```bash
# Via GitHub:
# https://vercel.com/
# Import project → ITPro100/barboss
```

## 📱 Інтеграція з соціальними мережами

### Instagram
Додайте посилання на сайт в профілі:
- @barbos_room
- @barbos_room_reserve  
- @barbos_delivery

### Telegram
Додайте посилання в:
- Канал @barbos_room
- Опис бота @Barbooss_bot
- Контакт @barbos_shop

## 🖼️ Додавання фото товарів

Завантажте реальні фото в:
```
/public/assets/products/  - Фото товарів
/public/assets/lookbook/  - Lifestyle фото
/public/assets/img/       - Загальні зображення
```

## 📝 Оновлення товарів

Редагуйте файл `content.json`:
```json
{
  "id": "unique-id",
  "name": "STONE ISLAND...",
  "brand": "Stone Island",
  "price": 21999,
  "currency": "грн",
  "sizes": ["M", "L", "XL"],
  "sold": false,
  "new": true
}
```

## 🎯 Приклад формату постів

```
STONE ISLAND GHOST PIECE JACKET
Size: M; L; XL
Price: 21999 грн🇺🇦
NEW
✅Worldwide shipping 🌎 
❌NOT SHIP TO russia 🇷🇺 

🏬BARBOSS SHOP 🏬

🇺🇦Україна, 
м.Київ, вул. Шота Руставели 27Б📍 

✏️По всім питанням пишіть:
@barbos_shop
```

## 🚀 Quick Deploy команди

```bash
# Clone repository
git clone https://github.com/ITPro100/barboss.git
cd barboss

# Test locally
python3 -m http.server 8000

# Deploy to Cloudflare (якщо встановлено wrangler)
npx wrangler pages deploy . --project-name=barboss-ukraine
```

## 📞 Підтримка

- Telegram: @barbos_shop
- Instagram: @barbos_room
- GitHub: https://github.com/ITPro100/barboss

---

**🇺🇦 Слава Україні! Всім мирного неба над головою 🫡**