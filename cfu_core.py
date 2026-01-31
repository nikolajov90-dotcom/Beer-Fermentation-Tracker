import matplotlib.pyplot as plt

def cfu_ml(colonies, dilution, plated_volume_ml):
    return colonies / (dilution * plated_volume_ml)


times = []
cfu_values = []

print("Unosi podatke po vremenskim tačkama.")
print("Za kraj unesi vreme -1.\n")

while True:
    time_point = float(input("Vreme uzorkovanja (h): "))
    
    if time_point == -1:
        break

    plate_results = []

    print("Unesi ploče za ovu vremensku tačku (0 kolonija = kraj).")

    while True:
        colonies = int(input("Broj kolonija: "))
        if colonies == 0:
            break
        
        dilution = float(input("Razblaženje (npr. 1e-5): "))
        volume = float(input("Zasejani volumen u mL (npr. 0.1): "))
        
        value = cfu_ml(colonies, dilution, volume)
        plate_results.append(value)
        
        print(f"CFU/mL: {value:.2e}\n")

    if plate_results:
        avg_value = sum(plate_results) / len(plate_results)
        times.append(time_point)
        cfu_values.append(avg_value)
        print(f"Prosek za {time_point} h: {avg_value:.2e}\n")


# crtanje krive
plt.figure()
plt.plot(times, cfu_values, marker="o")
plt.yscale("log")

plt.xlabel("Vreme fermentacije (h)")
plt.ylabel("CFU/mL (log skala)")
plt.title("Tok fermentacije – rast kvasca")
plt.grid(True)

plt.show()

