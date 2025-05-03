# This file contains fake data for database insertion and 
# for use in the app

products = (
        {
            "product_id":1,
            "image":"https://via.placeholder.com/500x700",
            "title":"Krita Pro",
            "description":"Графический редактор, позволяющий воплотить художественные мечты в жизнь.",
            "price":"2,990",
            "full_price":"2,990",
            "is_popular":1,
            "is_new":1,
        },
        {
            "product_id":2,
            "image":"https://via.placeholder.com/400x300",
            "title":"Inspire Pro",
            "description":"Фоторедактор для изображений с большим количеством он-лайн шаблонов, шрифтов и кистей для создания профессиональных изображений",
            "price":"2,990",
            "full_price":"2,990",
            "is_popular":1,
            "is_new":0,
        },
        {
            "product_id":3,
            "image":"https://via.placeholder.com/400x300",
            "title":"Muse Studio 2025 Professional",
            "description":"DAW для реальных профессионалов со встроенными инструментами и эффектами",
            "price":"2,990",
            "full_price":"5,990",
            "is_popular":1,
            "is_new":1,
        },
        {
            "product_id":4,
            "image":"https://via.placeholder.com/400x300",
            "title":"LibreOffice Commercial Edition",
            "description":"Коммерческая лицензия на использование LibreOffice",
            "price":"2,990",
            "full_price":"2,990",
            "is_popular":0,
            "is_new":0,
            "is_on_sale":0
        },
        {
            "product_id":5,
            "image":"https://via.placeholder.com/400x300",
            "title":"Greeva",
            "description":"Онлайн-доска для планирования и отслеживания выполнения задач в компании.",
            "price":"2,990",
            "full_price":"2,990",
            "is_popular":0,
            "is_new":1,
            "is_on_sale":0
        },
        {
            "product_id":6,
            "image":"https://via.placeholder.com/400x300",
            "title":"Epic VPN",
            "description":"VPN-сервис для корпоративного сектора",
            "price":"2,990",
            "full_price":"2,990",
            "is_popular":1,
            "is_new":1,
        },
        {
            "product_id":7,
            "image":"https://via.placeholder.com/400x300",
            "title":"Epic VPN Pro",
            "description":"Профессиональная версия VPN-сервиса для корпоративного сектора",
            "price":"5,999",
            "full_price":"10,990",
            "is_popular":1,
            "is_new":1,
        },
        {
            "product_id":8,
            "image":"https://via.placeholder.com/400x300",
            "title":"Нейрожириновский",
            "description":"Профессиональная программа для создания рекламных роликов с нейронной сетью Жириновского Владимира Вольфовича",
            "price":"99,999",
            "full_price":"99,990",
            "is_popular":1,
            "is_new":1,
        },
    )


nav_tabs = (
        {
            "status":1,
            "tab_name":"Все программы",
            "id":"all"
        },
        {
            "status":0,
            "tab_name":"Популярные",
            "id":"popular"
        },
        {
            "status":0,
            "tab_name":"Новые поступления",
            "id":"new"
        },
        {
            "status":0,
            "tab_name":"Скидки",
            "id":"on_sale"
        },
    )
