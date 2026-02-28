#include <algorithm>
#include <cmath>
#include <iostream>

using namespace std;

constexpr int r = 6356766;                               // m
constexpr double g0 = 9.81;                              // m/s^2
constexpr int R = 287.06;                                // J / (kg * K)
constexpr double sltemp = 288.15;                        // Kelvin
constexpr double slpressure = 101.325;                   // kPa
constexpr double sldensity = 1.225;                      // kg/m^3
constexpr double a1 = -6.5e-3;                           // K / m
constexpr double a2 = 3e-3;                              // K / m
constexpr double layer1alt = 11000;                      // m
constexpr double layer2alt = 25100;                      // m
constexpr double zero = 0;                               //
constexpr double isothermheight = layer2alt - layer1alt; // m
constexpr double isothermtemp = sltemp + layer1alt * a1; // Kelvin

extern "C" {

	__declspec(dllexport) double g(double h) {
		return g0 * pow(r / (r + h), 2);
    }

    __declspec(dllexport) double geopotential(double h) {
        return r * h / (r + h);
    }

    // determines the a value given a current height
    __declspec(dllexport) double currA(double h) {
        h = geopotential(h);
        return h >= layer2alt ? a2 : h <= layer1alt ? a1 : 0;
    }

    __declspec(dllexport) double temp(double h) {
        return sltemp + (h - max(zero, h - layer1alt)) * a1 + max(zero, h - layer2alt) * a2;
    }

    __declspec(dllexport) double pressure(double h) {
        h = geopotential(h);
        return slpressure * pow(temp(min(h, layer1alt)) / sltemp, -g0 / (a1 * R)) * exp(-g0 / (R * isothermtemp) *
        max(min(h - layer1alt, isothermheight), zero)) * pow((temp(max(h, layer2alt)) / isothermtemp), -g0 / (a2 * R) *
        max(h - layer2alt, zero) / (h - layer2alt));
    }

    __declspec(dllexport) double density(double h) {
        h = geopotential(h);
        return sldensity * pow(temp(min(h, layer1alt)) / sltemp, -g0 / (a1 * R) - 1) * exp(-g0 / (R * isothermtemp) *
        max(min(h - layer1alt, isothermheight), zero)) * pow((temp(max(h, layer2alt)) / isothermtemp), (-g0 / (a2 * R) - 1) *
        max(h - layer2alt, zero) / (h - layer2alt));
    }


    __declspec(dllexport) double sos(double h) {
        return pow(1.4 * R * temp(h), 0.5);
    }
}