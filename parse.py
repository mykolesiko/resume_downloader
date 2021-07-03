from functools import wraps
from datetime import datetime

MONTHS = {"Январь": "January",
          "Февраль": "February",
          "Март": "March",
          "Апрель": "April",
          "Май": "May",
          "Июнь": "June",
          "Июль": "July",
          "Август": "August",
          "Сентябрь": "September",
          "Октябрь": "October",
          "Ноябрь": "November",
          "Декабрь": "December"}


def num_pages(page):
    """
    :param bs4.BeautifulSoup page: resumes search page
    :return: int
    """
    num = page.find("div", {"data-qa": "pager-block"})

    if not num:
        return 1

    num = num.findAll("a", {"class": "bloko-button"})

    if not num:
        return 1

    return int(num[-2].getText())


def resume_hashes(page):
    print("in resume hashes")
    """
    :param bs4.BeautifulSoup page: resumes search page
    :return: list
    """
    hashes = []
    page = page.find("div", {"data-qa": "resume-serp__results-search"})
    #print(page)

    if page is not None:
        hashes = page.findAll("div", {"data-qa": "resume-serp__resume"})
        #print(hashes)
        hashes = [item.find("a")["href"][8:46] for item in hashes]
    #print(hashes)
    return hashes


def header(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"class": "resume-header-block"})


def get_optional_text(find_optional_element):
    @wraps(find_optional_element)
    def wrapper(page):
        """
        :param bs4.Tag element: element from resume
        :return: str or None
        """
        optional_element = find_optional_element(page)
        return None if optional_element is None else optional_element.getText()
    return wrapper


@get_optional_text
def birth_date(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str or None
    """
    return page.find("span", {"data-qa": "resume-personal-birthday"})


#<div class="resume-header-title"><div class="resume-header-photo-mobile" data-qa="resume-photo-mobile"><div class="resume-photo resume-photo_empty"><div class="resume-photo__placeholder"><a class="bloko-link bloko-link_secondary" data-qa="resume-add-photo" href="/applicant/resumes/edit/photo?resume=fca5698aff08aa635d0039ed1f447631434632">Добавить фото</a></div></div></div><div class="resume-online-status resume-online-status_online">Сейчас на&nbsp;сайте</div><div class="resume-header-name"><h2 data-qa="resume-personal-name" class="bloko-header-1"><span>Иванова Елена</span></h2></div><p><span data-qa="resume-personal-gender">Женщина</span>, <span data-qa="resume-personal-age">42&nbsp;года</span>, родилась&nbsp;<span data-qa="resume-personal-birthday">20&nbsp;июня&nbsp;1978</span></p><p><a data-qa="resume-block-personal-edit" class="resume-block-edit resume-block-edit_capitalize" href="/applicant/resumes/edit/personal?resume=fca5698aff08aa635d0039ed1f447631434632">редактировать</a></p><div class="resume-header-field"><div data-qa="resume-block-contacts"><p class="resume-contacts-title">Контакты</p><div class="resume-search-item__description-content" data-qa="resume-serp_resume-item-content"><div data-qa="resume-contacts-phone"><span>+7 (903) 619-30-72</span><div class="bloko-translate-guard">&nbsp;<button type="button" class="bloko-icon-link"><span class="bloko-icon bloko-icon_warning bloko-icon_initial-impact"></span></button></div></div></div><div data-qa="resume-contact-email"><a href="mailto:ivelena1234567@mail.ru" data-qa="resume-contact-preferred"><span>ivelena1234567@mail.ru</span></a>&nbsp;— предпочитаемый способ связи</div><p><a data-qa="resume-block-contacts-edit" class="resume-block-edit resume-block-edit_capitalize" href="/applicant/resumes/edit/contacts?resume=fca5698aff08aa635d0039ed1f447631434632">редактировать</a></p></div></div><p><span data-qa="resume-personal-address">Москва</span>, <span data-qa="resume-personal-metro" style="color: rgb(0, 114, 186);">м.&nbsp;Первомайская</span>, готова к переезду, готова к командировкам</p><p><a data-qa="resume-block-personal-edit" class="resume-block-edit resume-block-edit_capitalize" href="/applicant/resumes/edit/personal?resume=fca5698aff08aa635d0039ed1f447631434632">редактировать</a></p><div class="resume-header-print-update-date">Резюме обновлено&nbsp;29.01.2021 09:02</div></div>
#@get_optional_text
def move_trips(page):
    page = page.find("div", {"class" : "resume-header-title"})
    if page is not None:
        page = page.find("div", {"class" : "resume-header-field"})
        print(page.getText())
        p = page.next_sibling()
        print(p)
        #if p is not None:
        #    print(p)
        #    items = p.find_all()
        #    for item in items:
        #        print(item)
        #        if item.name != "span":
        #            print(item.getText())


    return p.getText()               



@get_optional_text
def gender(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str or None
    """
    return page.find("span", {"data-qa": "resume-personal-gender"})


def check_and_get_text(elem): 
    if elem is not None:
        return elem.getText()
    else:
        return ""    



@get_optional_text
def area(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str or None
    """
    return page.find("span", {"data-qa": "resume-personal-address"})

def phone(page):
   #<div data-qa="resume-contacts-phone"><span>+7 (903) 619-30-72</span><div class="bloko-translate-guard">&nbsp;<button type="button" class="bloko-icon-link"><span class="bloko-icon bloko-icon_warning bloko-icon_initial-impact"></span></button></div></div>
    return check_and_get_text(page.find("div", {"data-qa" : "resume-contacts-phone"}))

def email(page):
    page = page.find("div", {"data-qa":"resume-contact-email"})
    mail = None
    if page is not None:
        mail = page.find("a")
    return check_and_get_text(mail)
#<div data-qa="resume-contact-email"><a href="mailto:ivelena1234567@mail.ru" data-qa="resume-contact-preferred"><span>ivelena1234567@mail.ru</span></a>&nbsp;— предпочитаемый способ связи</div>    


#<span data-qa="resume-personal-metro" style="color: rgb(0, 114, 186);">м.&nbsp;Первомайская</span>
def metro(page):
    print("1")
    metro = page.find('span', {"data-qa":"resume-personal-metro"})
    print (metro)
    str = check_and_get_text(metro)
    print(str)
    return  str

def prava(page):
    list_prava = []
    #<div data-qa="resume-block-driver-experience" class="resume-block"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"><div class="resume-block-container"><h2 data-qa="bloko-header-2" class="bloko-header-2 bloko-header-2_lite"><span class="resume-block__title-text resume-block__title-text_sub">Опыт вождения</span><a data-qa="resume-block-driver-experience-edit" class="resume-block-edit resume-block-edit_capitalize" href="/applicant/resumes/edit/experience?resume=fca5698aff08aa635d0039ed1f447631434632&amp;field=driverLicenseTypes">редактировать</a></h2></div></div></div><div class="resume-block-item-gap"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"><div class="resume-block-container">Права категории&nbsp;A</div></div></div></div></div>
    page = page.find("div", { "data-qa" :"resume-block-driver-experience"})
    print(page)
    if page is None:
        return list_prava
    #<div class="resume-block-item-gap"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"><div class="resume-block-container">Права категории&nbsp;A</div></div></div></div>        
    page = page.find("div", {"class" : "resume-block-item-gap"})
    print(page)
    if page is None:
        return list_prava
    
    page = page.find("div",  {"class" : "resume-block-container"})
    print(page)
    if page is None:
        return list_prava
    
    
    prava = {}
    print(page.getText())
    prava.update({"prava1":check_and_get_text(page)})
    p = page.find("p")
    print(p)
    if p is not None:
        prava.update({"prava2":check_and_get_text(p)})
    list_prava.append(prava)
    return list_prava

def position(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"class": "resume-block", "data-qa": "resume-block-position"})


def position_title(position_block):
    """
    :param bs4.Tag position_block: position block
    :return: str
    """
    title = position_block.find("span", {"class": "resume-block__title-text",
                                         "data-qa": "resume-block-title-position"})

    return title.getText()


def position_specializations(position_block):
    """
    :param bs4.Tag position_block: position block
    :return: list
    """
    position_block = position_block.find("div", {"class": "bloko-gap bloko-gap_bottom"})

    profarea_name = position_block.find("span", {"data-qa": "resume-block-specialization-category"})
    profarea_name = profarea_name.getText()

    profarea_specializations = position_block.find("ul")
    profarea_specializations = profarea_specializations.findAll("li", {"class": "resume-block__specialization",
                                                                       "data-qa": "resume-block-position-specialization"})

    profarea_specializations = [item.getText() for item in profarea_specializations]
    profarea_specializations = [{"name": specialization_name, "profarea_name": profarea_name}
                                for specialization_name in profarea_specializations]

    return profarea_specializations

#@get_optional_text
def portfolio(page):
    #<div data-qa="resume-block-portfolio" class="resume-block"><div class="bloko-columns-row">
    # <div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12">
    # <div class="resume-block-container"><h2 data-qa="bloko-header-2" class="bloko-header-2 bloko-header-2_lite">
    # <span class="resume-block__title-text resume-block__title-text_sub">Портфолио</span>
    # <a data-qa="resume-block-portfolio-edit" class="resume-block-edit resume-block-edit_capitalize" href="/applicant/resumes/edit/experience?resume=fca5698aff08aa635d0039ed1f447631434632&amp;field=portfolio">редактировать</a></h2></div></div></div><div class="resume-block-item-gap"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"><div class="resume-block-container"><div class="form__popup m-resume_portfolio"><div class="resume-block__portfolio-wrapper"><a class="resume__portfolio-item"><img src="https://hhcdn.ru/photo/610127889.png?t=1612012337&amp;h=ALkfOGpJ6aCIMQZFsV_j2Q" loading="lazy" alt=""></a></div></div></div></div></div></div></div>    
    page  = page.find("div", {"data-qa":"resume-block-portfolio", "class":"resume-block"})
    
    portfolio_items = {}
    if page is not None:
        items = page.find_all("a",  {"class" : "resume__portfolio-item"})
        s = 0
        for item in items:
            if item is not None:
                page = item.find("img")
                if page is not None:
                    print(page["src"])
                    portfolio_items.update({f"portfolio_item {s}" : page["src"]})
                    s += 1
    return  portfolio_items   

def position_salary(position_block):
    """
    :param bs4.Tag position_block: position block
    :return: dict
    """
    salary = position_block.find("span", {"class": "resume-block__salary resume-block__title-text_salary",
                                          "data-qa": "resume-block-salary"})
    amount = None
    currency = None
    if salary is not None:
        salary = salary.getText().replace('\u2009', '').replace('\xa0', ' ').strip().split()
        amount = int(salary[0])
        currency = ' '.join(salary[1:])

    salary = {"amount": amount,
              "currency": currency}

    return salary


#def desired_vacancy(page):
    #<span class="resume-block__title-text" data-qa="resume-block-title-position"><span>Data Scientist</span></span>
#    item = page.find("span", {class="resume-block__title-text" data-qa="resume-block-title-position"})
#    return item.getText() 


def education(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"class": "resume-block", "data-qa": "resume-block-education"})


def education_level(education_block):
    """
    :param bs4.Tag education_block: education block
    :return: str
    """
    if education_block is not None:
        return education_block.find("span", {"class": "resume-block__title-text resume-block__title-text_sub"}) \
                              .getText()

    return "Образования нет"


def educations(education_block):
    """
    :param bs4.Tag education_block: education block
    :return: list
    """
    page_educations = []
    if education_block is not None:
        education_block = education_block.find("div", {"class": "resume-block-item-gap"}) \
                                         .find("div", {"class": "bloko-columns-row"})

        for education_item in education_block.findAll("div", {"class": "resume-block-item-gap"}):
            year = education_item.find("div", {"class": "bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2"}) \
                                 .getText()

            item_name = education_item.find("div", {"data-qa": "resume-block-education-name"}) \
                                      .getText()

            item_organization = education_item.find("div", {"data-qa": "resume-block-education-organization"})
            if item_organization is not None:
                item_organization = item_organization.getText()
                
            page_educations.append(
                {"year": int(year),
                 "name": item_name,
                 "faculty, speciality": item_organization}
                 
            )

    return page_educations


def languages(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: list
    """
    page_languages = []
    page = page.find("div", {"class": "resume-block", "data-qa": "resume-block-languages"})

    if page is not None:
        for language in page.findAll("p", {"data-qa": "resume-block-language-item"}):
            language = language.getText().split(" — ")

            level = ' - '.join(language[1:])
            language = language[0]

            page_languages.append({"name": language,
                                   "level": level})

    return page_languages


def date(date, format="%d-%m-%Y"):
    """
    :param date str: date in format "Month (russian) Year"
    :param format str: desired data format
    :return: str
    """
    if date in ["по настоящее время", "currently"]:
        return None

    month, year = date.split()

    if month in MONTHS:
        month = MONTHS[month]

    date = f"{month} {year}"
    date = datetime.strptime(date, "%B %Y").strftime(format)

    return date


def experiences(page, format="%d-%m-%Y"):
    """
    :param bs4.BeautifulSoup page: resume page
    :param format str: desired data format
    :return: list
    """
    #print("in experience")

    page_experiences = []
    page = page.find("div", {"class": "resume-block", "data-qa": "resume-block-experience"})

    if page is not None:
        page = page.find("div", {"class": "resume-block-item-gap"})
        for experience_item in page.findAll("div", {"class": "resume-block-item-gap"}):
            time_interval = experience_item.find("div", {"class": "bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2"})
            time_interval.div.extract()

            start, end = time_interval.getText().replace("\xa0", " ").split(' — ')
            
            #<div class="bloko-text-emphasis"><span>PAO Rosbank Societe Generale Group</span></div>
            company = experience_item.find("div",  {"class": "bloko-text-emphasis"})
            company = "" if company is None else company.getText()
            #print(company)

            #<div data-qa="resume-block-experience-position" class="bloko-text-emphasis"><span></span><span class="highlighted">IT</span><span> Support Officer</span></div>
            #item_position = experience_item.find("div",  {"class": "resume-block__sub-title", "data-qa": "resume-block-experience-position"})
            item_position = experience_item.find("div",  {"class": "bloko-text-emphasis", "data-qa": "resume-block-experience-position"})
            item_position = "" if item_position is None else item_position.getText()
            #print(f"item = {item_position}")

            item_description = experience_item.find("div", {"data-qa": "resume-block-experience-description"})
            description_child = item_description.findChild()
            item_description = item_description.getText() if description_child is None else str(description_child)
            
     
            page_experiences.append(
                {"start": date(start, format=format),
                 "end": date(end, format=format),
                 "company": company,
                 "position": item_position,
                 "description": item_description}
            )

    return page_experiences


def attestation(page, format="%d-%m-%Y"):
    """
    :param bs4.BeautifulSoup page: resume page
    :param format str: desired data format
    :return: list
    """
    #print("in experience")

    page_attestation = []
    page = page.find("div", {"class": "resume-block", "data-qa": "resume-block-attestation-education"})

    if page is not None:
        for item in page.find_all("div", {"class": "resume-block-item-gap"}):
            if item is not None:

                #<div class="bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2">2006</div>
                page1 = item.find("div", {"class": "bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2"})
                if page1 is not None:
                    year = "" if page1 is None else page1.getText()
                    #<div class="bloko-column bloko-column_xs-4 bloko-column_s-6 bloko-column_m-7 bloko-column_l-10"><div class="resume-block-container" data-qa="resume-block-education-item"><div data-qa="resume-block-education-name" class="bloko-text-emphasis"><span>MIPT</span></div><div data-qa="resume-block-education-organization"><span>Coursera</span><span>, </span><span>DataScientist</span></div></div></div>
                    #<div class="resume-block-container" data-qa="resume-block-education-item"><div data-qa="resume-block-education-name" class="bloko-text-emphasis"><span>MIPT</span></div><div data-qa="resume-block-education-organization"><span>Coursera</span><span>, </span><span>DataScientist</span></div></div>
                page2 = item.find("div", {"class": "bloko-column bloko-column_xs-4 bloko-column_s-6 bloko-column_m-7 bloko-column_l-10"})
                if page2 is not None: 
                    page2 =  page2.find("div", {"class": "resume-block-container", "data-qa" : "resume-block-education-item"})
                    name = page2.find("div" , {"data-qa" : "resume-block-education-name"})
                    name = "" if name is None else name.getText()
                    print(name)

                    education_org = page2.find("div", {"data-qa":"resume-block-education-organization"})
                    education_org = "" if education_org is None else education_org.getText()
                    #print(f"item = {item_position}")

            
     
            page_attestation.append(
                {"year": year,
                 "institution": name,
                 "organization_specialization": education_org}
            )

    return page_attestation




def additional(page): 
    page_add = []
    #<div data-qa="resume-block-additional" class="resume-block"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"><div class="resume-block-container"><h2 data-qa="bloko-header-2" class="bloko-header-2 bloko-header-2_lite"><span class="resume-block__title-text resume-block__title-text_sub">Гражданство, время в пути до работы</span><a data-qa="resume-block-additional-edit" class="resume-block-edit resume-block-edit_capitalize" href="/applicant/resumes/edit/additional?resume=fca5698aff08aa635d0039ed1f447631434632">редактировать</a></h2></div></div></div><div class="resume-block-item-gap"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"><div class="resume-block-container"><p>Гражданство: Россия</p><p>Разрешение на работу: Россия</p><p>Желательное время в пути до работы: <span class="resume-block-travel-time">Не имеет значения</span></p></div></div></div></div></div>
    page = page.find("div", {"class": "resume-block", "data-qa":"resume-block-additional"})
    
    dop = {}
    if page is not None:
        page = page.find("div", {"class": "resume-block-item-gap"})    
        if page is not None:
            page = page.find("div", {"class":"resume-block-container"})    
            print("1")
            if page is not None:
                print(page)    
                s = 0
                for item in page.findAll("p"):
                    if item is not None:
                        print("1")
                        dop.update({f"dop {s + 1}":item.getText()})
                        s += 1
    page_add.append(dop)
    return  page_add  


def recommendations(page): 
    page_recom = []
    #<div data-qa="resume-block-additional" class="resume-block"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"><div class="resume-block-container"><h2 data-qa="bloko-header-2" class="bloko-header-2 bloko-header-2_lite"><span class="resume-block__title-text resume-block__title-text_sub">Гражданство, время в пути до работы</span><a data-qa="resume-block-additional-edit" class="resume-block-edit resume-block-edit_capitalize" href="/applicant/resumes/edit/additional?resume=fca5698aff08aa635d0039ed1f447631434632">редактировать</a></h2></div></div></div><div class="resume-block-item-gap"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"><div class="resume-block-container"><p>Гражданство: Россия</p><p>Разрешение на работу: Россия</p><p>Желательное время в пути до работы: <span class="resume-block-travel-time">Не имеет значения</span></p></div></div></div></div></div>
    page = page.find("div", {"class": "resume-block", "data-qa":"resume-block-recommendation"})
    print("rec")
    recommendations = {}
    if page is not None:
        page = page.find("div", {"class": "resume-block-item-gap"})    
        if page is not None:
            page = page.find("div", {"class":"resume-block-container"})    
            if page is not None:
                print(page)    
                s = 0
                str = ""
                for item in page.findAll("div"):
                    if item is not None:
                        print(s)
                        print(item)
                        if s % 2 == 0:
                            str = item.getText()
                        else :
                            str = str +  " " + item.getText()  
                            recommendations.update({f"recommendation {s//2 + 1}" : str})
                        s += 1
    page_recom.append(recommendations)
    return  page_recom  

def certificates2(page): 
    page_certs = []
    #<div data-qa="resume-block-additional" class="resume-block"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"><div class="resume-block-container"><h2 data-qa="bloko-header-2" class="bloko-header-2 bloko-header-2_lite"><span class="resume-block__title-text resume-block__title-text_sub">Гражданство, время в пути до работы</span><a data-qa="resume-block-additional-edit" class="resume-block-edit resume-block-edit_capitalize" href="/applicant/resumes/edit/additional?resume=fca5698aff08aa635d0039ed1f447631434632">редактировать</a></h2></div></div></div><div class="resume-block-item-gap"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"><div class="resume-block-container"><p>Гражданство: Россия</p><p>Разрешение на работу: Россия</p><p>Желательное время в пути до работы: <span class="resume-block-travel-time">Не имеет значения</span></p></div></div></div></div></div>
    page = page.find("div", {"class": "resume-block", "data-qa":"resume-block-certificate"})
    if page is None:
        return []
    print("rec")
    certs = {}
    s = 0
    #<div class="resume-certificates-view__year-group"><div class="resume-certificates-view__year-group-title">2010</div><ul class="resume-certificates-view__items"><li class="resume-certificates-view__item"><span class="resume-certificates-view__item-title"><a target="_blank" rel="noopener noreferrer" href="http://345435.ru">certificate2</a></span></li></ul></div>
    for item in page.findAll("div",  {"class" : "resume-certificates-view__year-group"}):
        if item is not None:
            print(item)
            #<div class="resume-certificates-view__year-group-title">2010</div>
            year = item.find("div",  {"class" : "resume-certificates-view__year-group-title"})
            if year is not None:
                year = "" if year is None else year.getText()
                certs.update({"year" : year})            
            page2 = item.find("ul",  {"class" : "resume-certificates-view__items"})
            if page2 is not None:
                name_link = page2.find("a")
                name = "" if name_link is None else name_link.getText()
                certs.update({"name" : name})            
                certs.update({"link" : name_link["href"]})      
            page_certs.append(certs)
    
    return  page_certs





def certificates(page):#, format="%d-%m-%Y"):
    """
    :param bs4.BeautifulSoup page: resume page
    :param format str: desired data format
    :re: list
    
    """
    #print("1")
    page_dop = []

    #<div data-qa="resume-block-additional-education" class="resume-block"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-9 bloko-column_l-12"><div class="resume-block-container"><h2 data-qa="bloko-header-2" class="bloko-header-2 bloko-header-2_lite"><span class="resume-block__title-text resume-block__title-text_sub">Повышение квалификации, курсы</span><a data-qa="resume-block-additional-education-edit" class="resume-block-edit resume-block-edit_capitalize" href="/applicant/resumes/edit/education?resume=fca5698aff08aa635d0039ed1f447631434632&amp;field=additionalEducation">редактировать</a></h2></div></div></div><div class="resume-block-item-gap"><div class="bloko-columns-row"><div class="resume-block-item-gap"><div class="bloko-columns-row"><div class="bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2">2004</div><div class="bloko-column bloko-column_xs-4 bloko-column_s-6 bloko-column_m-7 bloko-column_l-10"><div class="resume-block-container" data-qa="resume-block-education-item"><div data-qa="resume-block-education-name" class="bloko-text-emphasis"><span>MIPT</span></div><div data-qa="resume-block-education-organization"><span>Coursera</span><span>, </span><span>DataScientist</span></div></div></div></div></div></div></div></div>
    page = page.find("div", {"class": "resume-block", "data-qa": "resume-block-additional-education"})

    if page is not None:
        #print("1")
        page = page.find("div", {"class": "resume-block-item-gap"})
        #print("1")
        for item in page.findAll("div", {"class": "resume-block-item-gap"}):

            #print("1")    
            #<div class="bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2">2003</div>
            year = item.find("div", {"class": "bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2"})
            #print(year)
            year.extract()
            year_str = check_and_get_text(year)
            #print(year_str)
            
            #<div data-qa="resume-block-education-name" class="bloko-text-emphasis"><span>Coursera</span></div>
            company = item.find("div",  {"class": "bloko-text-emphasis", "data-qa": "resume-block-education-name"})
            company = "" if company is None else company.getText()
            #print(company)



            #<div data-qa="resume-block-education-organization"><span>Coursera</span><span>, </span><span>DataScientist</span></div>
            org_spec = item.find("div", {"data-qa":"resume-block-education-organization"})
            org_spec = "" if org_spec is None else org_spec.getText()
            #print(specialization)
            #org, spec = org_spec.strip().split(",")


            #<div data-qa="resume-block-education-organization"><!-- --><!-- --><span>Coursera</span><span>, </span><span>DataScientist</span></div>
            #<span>Coursera</span>
            #item_description = experience_item.find("div", {"data-qa": "resume-block-experience-description"})
            #description_child = item_description.findChild()
            #item_description = item_description.getText() if description_child is None else str(description_child)

            page_dop.append(
                {"year" : year_str,
                 "institution" : company,
                 "organization + specialization" : org_spec


                }
            )

    return page_dop

def skill_set(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: list
    """
    page = page.find("div", {"data-qa": "skills-table", "class": "resume-block"})

    page_skill_set = []
    if page is not None:
        page_skill_set = page.findAll("div", {"class": "bloko-tag bloko-tag_inline bloko-tag_countable",
                                              "data-qa": "bloko-tag bloko-tag_inline"})
        page_skill_set = [skill.getText() for skill in page_skill_set]

    return page_skill_set


def skills(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str
    """
    page = page.find("div", {"data-qa": "resume-block-skills-content"})

    page_skills = ""
    if page is not None:
        skills_child = page.findChild()
        page_skills = page.getText() if skills_child is None else str(skills_child)

    return page_skills


#Место работы (название компании)
#Должность
#период работы
#Желаемая должность
#Университет (название)
#Специальность (кафедра)


def resume(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: dict
    """
    #print("***********************")
    page = page.find("div", {"id": "HH-React-Root"})

    resume_position = position(page)
    resume_education = education(page)

    return {
        "birth_date": birth_date(page),
        "gender": gender(page),
        "area": area(page),
        "phone":phone(page),
        "email": email(page),
        "metro": metro(page),
        "prava": prava(page),
        #"move_trips": move_trips(page),
        "title": position_title(resume_position),
        "specialization": position_specializations(resume_position),
        "salary": position_salary(resume_position),
        "education_level": education_level(resume_education),
        "education": educations(resume_education),
        "courses": certificates(page),
        "certificates": certificates2(page),
        "language": languages(page),
        "experience": experiences(page),
        "skill_set": skill_set(page),
        "skills": skills(page),
        "recommendations" : recommendations(page),
        "attestation" : attestation(page),
        "dop_info": additional(page),
        "portfolio": portfolio(page)
    }

    return resume
