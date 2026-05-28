# Hur tar jag fram rapport till Bygglösen i HRM Payroll?

**Datum:** den 5 maj 2026  
**Kategori:** Payroll  
**Underkategori:** Löneberedning  
**Typ:** howto  
**Svårighetsgrad:** intermediate  
**Tags:** lön, löneart  
**Bilder:** 7  
**URL:** https://knowledge.flexhrm.com/sv/hur-rapporterar-jag-byggl%C3%B6sen-i-hrm-payroll

---

Denna artikel beskriver hur du tar ut rapport för Bygglösen i systemet.
Skapa underlag
Skapa fil för rapportering
Vilka medarbetare innehåller underlaget
Så här skapar du ett nytt underlag
Det första steget i rapporteringen är att skapa ett underlag för den månad som rapporteringen gäller.
Gå till
Administration
>
Bearbetningar
>
Statistikrapportering
>
Bygglösen
.
Klicka på knappen
Ny
i knappraden.
![Knappen Ny visas markerad.](images/hur-tar-jag-fram-rapport-till-bygglosen-i-hrm-payroll_36dce047.png)
Välj aktuell
redovisningsperiod,
t.ex. om du ska redovisa utbetald lön och timmar för mars månad har dessa löneberäknats i april lön, då väljer du period 1-30 april.
Observera:
Om du använder bruten löneperiod ska du skapa underlaget för den motsvarande perioden, t.ex 16/4-15/5.
Om det behövs kan du även göra kompletterande urval för att begränsa underlaget.
![Bild](images/hur-tar-jag-fram-rapport-till-bygglosen-i-hrm-payroll_670469c2.png)
I det färdiga underlaget kan en medarbetare redovisas på flera rader. Det händer till exempel om hen har utfört arbete i olika län eller med olika kommunkoder.
![Bild](images/hur-tar-jag-fram-rapport-till-bygglosen-i-hrm-payroll_f3e4822c.png)
Du kan också exportera underlaget till Excel genom att klicka på knappen
Excel
i knappraden.
![Bilden visar knappen för att exportera underlaget till Excel..](images/hur-tar-jag-fram-rapport-till-bygglosen-i-hrm-payroll_c0816be7.png)
När underlaget är granskat markerar du underlaget som kontrollerat genom att klicka på knappen
Markera som kontrollerad
.
![Bilden visar knappen "Markera som kontrollerad".](images/hur-tar-jag-fram-rapport-till-bygglosen-i-hrm-payroll_4056c9bc.png)
Underlaget får då statusen
Kontrollerad
. Systemet sparar även datum, tid och användarsignatur för den som genomfört kontrollmarkeringen.
![Bilden visar fälten för status, datum och tid samt signatur.](images/hur-tar-jag-fram-rapport-till-bygglosen-i-hrm-payroll_04610c0f.png)
Om du hittar ett fel i ett kontrollerat underlag kan du ta bort kontrollmarkeringen igen, vilket gör att statusen återigen blir preliminär.
Fil för redovisning
När underlaget har sammanställts genereras automatiskt en rapportfil. Denna fil underlättar rapporteringen till och kan hämtas via knappen
Visa filer
i knappraden.
![Bilden visar knappen för att visa filer.](images/hur-tar-jag-fram-rapport-till-bygglosen-i-hrm-payroll_9694260e.png)
Listan över filer innehåller en fil per redovisningsperiod, där den senaste ligger överst. Filen finns tillgänglig tills du väljer att ta bort underlaget i huvudvyn. Ladda ner filen genom att klicka på ikonen och skicka in den.
Vilka medarbetare inkluderas i rapporten?
För att en medarbetare ska komma med i underlaget behöver följande två kriterier vara uppfyllda:
Medarbetaren tillhör en personalkategori som är kopplad till ett avtalsområde.
Medarbetaren har registrerade arbetade timmar i lönekörningen. Detta innebär att det finns en löneart som har markeringen för arbetad tid.
Hur hämtas värden till rapporten?
Kolumn
Var värdet kommer ifrån
Arbetsplatsnummer
Vid prestationslön: projektets arbetsplatsnummer via kontering på transaktion. Rader grupperas på detta värde när det är relevant.
Avtalsområde
Avtalsområde på personalkategorin för den senaste anställningsperioden inom datumintervallet.
Fördelningstal
Värde från anställningens numeriska fält som är markerat som fördelningstal.
Lönetyp
Tidlön eller Prestationslön utifrån inställning på projekt.
Arbetade timmar
Summa av antal timmar på transaktioner lönearten är markerad med Bygglösen - Arbetade timmar.
Grundlön per timma
Vid prestationslön: Avtalad timlön enligt anställdaregistret med hänsyn tagen till gällande fördelningstal.
Utbetalningsnivå per timma
Vid prestationslön: Från projektets inställning med hänsyn tagen till fördelningstal.
Utbetalt ackordsöverskott
Summa belopp där lönearten är markerad med Bygglösen - Avser ackordsöverskott, men bara om det finns arbetade timmar på samma arbetsplats i underlaget; annars tomt.
Lönesumma
Summa belopp från transaktioner där lönearten är markerad med Bygglösen - Avser utbetald lön.
Avtalad månadslön
Senast gällande månadslön inom datumintervall från anställdaregistret. Enbart för månadsavlönade.
Övertidstimmar
Summa av timmar från transaktioner där lönearten är markerad med Bygglösen - Övertidstimmar.
Övertidstillägg
Summa belopp från transaktioner där lönearten är markerad med Bygglösen - Övertidstillägg.
OB-tillägg
Summa belopp från transaktioner där lönearten är markerad med Bygglösen - OB-tillägg.
Byggarbetsplatsens län och kommun
Från konteringskod för län och kommun på transaktionens kontering.
Yrkeskod
Fältet Yrkeskod (NYK14) i anställdaregistret på senaste anställningsperioden inom datumintervall.
Relaterade artiklar:
Vilka inställningar behövs för att kunna rapportera Bygglösen i HRM Payroll
