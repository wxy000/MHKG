# -*- coding: utf-8 -*-
import time

log_path = "/root/MHKG/Django/logs/"


class Toolbar:
    def filesize(self, size):
        kb = 1024
        mb = kb * 1024
        gb = mb * 1024
        tb = gb * 1024

        if size <= kb:
            return str(round(size, 2)) + 'B'
        elif size <= mb:
            return str(round(size / kb, 2)) + 'KB'
        elif size <= gb:
            return str(round(size / mb, 2)) + 'MB'
        elif size <= tb:
            return str(round(size / gb, 2)) + 'GB'
        else:
            return str(round(size / tb, 2)) + 'TB'

    def openfile(self):
        ips = []
        sum_bytes = 0
        sum_code = 0
        with open(log_path + 'nginx_access.log', 'r') as f:
            for line in f:
                ip = line.split(' ')[0]
                if line.split(' ')[9].isdigit():
                    bodyBytesSent = int(line.split(' ')[9])
                else:
                    bodyBytesSent = 0
                sum_bytes += bodyBytesSent
                if line.split(' ')[8] == '200':
                    sum_code += 1
                ips.append(ip)
        lenips = len(ips)
        if len(ips) == 0:
            lenips = 1
        sum_code_ratio = str(round((sum_code / lenips) * 100, 2)) + '%'
        temp = {'pv_now': len(ips), 'uv_now': len(set(ips)), 'byte_now': self.filesize(sum_bytes),
                'code_ratio_now': sum_code_ratio}
        return temp

    def parsetime(self, log_time, d):
        time_str = '%s' % log_time
        if d == 'today':
            return time.strftime("%H:%M:%S", time.strptime(time_str, '%d/%b/%Y:%H:%M:%S'))
        else:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time_str, '%d/%b/%Y:%H:%M:%S'))

    def openfile_pul(self):
        time_005 = list()
        time_010 = list()
        time_015 = list()
        time_020 = list()
        time_025 = list()
        time_030 = list()
        time_035 = list()
        time_040 = list()
        time_045 = list()
        time_050 = list()
        time_055 = list()
        time_060 = list()
        time_065 = list()
        time_070 = list()
        time_075 = list()
        time_080 = list()
        time_085 = list()
        time_090 = list()
        time_095 = list()
        time_100 = list()
        time_105 = list()
        time_110 = list()
        time_115 = list()
        time_120 = list()
        time_125 = list()
        time_130 = list()
        time_135 = list()
        time_140 = list()
        time_145 = list()
        time_150 = list()
        time_155 = list()
        time_160 = list()
        time_165 = list()
        time_170 = list()
        time_175 = list()
        time_180 = list()
        time_185 = list()
        time_190 = list()
        time_195 = list()
        time_200 = list()
        time_205 = list()
        time_210 = list()
        time_215 = list()
        time_220 = list()
        time_225 = list()
        time_230 = list()
        time_235 = list()
        time_000 = list()

        with open(log_path + 'nginx_access.log', 'r') as f:
            for line in f:
                log_time = self.parsetime(line.split(' ')[3][1:], 'today')
                if log_time < '00:30:00':
                    time_000.append(line)
                elif log_time < '01:00:00':
                    time_005.append(line)
                elif log_time < '01:30:00':
                    time_010.append(line)
                elif log_time < '02:00:00':
                    time_015.append(line)
                elif log_time < '02:30:00':
                    time_020.append(line)
                elif log_time < '03:00:00':
                    time_025.append(line)
                elif log_time < '03:30:00':
                    time_030.append(line)
                elif log_time < '04:00:00':
                    time_035.append(line)
                elif log_time < '04:30:00':
                    time_040.append(line)
                elif log_time < '05:00:00':
                    time_045.append(line)
                elif log_time < '05:30:00':
                    time_050.append(line)
                elif log_time < '06:00:00':
                    time_055.append(line)
                elif log_time < '06:30:00':
                    time_060.append(line)
                elif log_time < '07:00:00':
                    time_065.append(line)
                elif log_time < '07:30:00':
                    time_070.append(line)
                elif log_time < '08:00:00':
                    time_075.append(line)
                elif log_time < '08:30:00':
                    time_080.append(line)
                elif log_time < '09:00:00':
                    time_085.append(line)
                elif log_time < '09:30:00':
                    time_090.append(line)
                elif log_time < '10:00:00':
                    time_095.append(line)
                elif log_time < '10:30:00':
                    time_100.append(line)
                elif log_time < '11:00:00':
                    time_105.append(line)
                elif log_time < '11:30:00':
                    time_110.append(line)
                elif log_time < '12:00:00':
                    time_115.append(line)
                elif log_time < '12:30:00':
                    time_120.append(line)
                elif log_time < '13:00:00':
                    time_125.append(line)
                elif log_time < '13:30:00':
                    time_130.append(line)
                elif log_time < '14:00:00':
                    time_135.append(line)
                elif log_time < '14:30:00':
                    time_140.append(line)
                elif log_time < '15:00:00':
                    time_145.append(line)
                elif log_time < '15:30:00':
                    time_150.append(line)
                elif log_time < '16:00:00':
                    time_155.append(line)
                elif log_time < '16:30:00':
                    time_160.append(line)
                elif log_time < '17:00:00':
                    time_165.append(line)
                elif log_time < '17:30:00':
                    time_170.append(line)
                elif log_time < '18:00:00':
                    time_175.append(line)
                elif log_time < '18:30:00':
                    time_180.append(line)
                elif log_time < '19:00:00':
                    time_185.append(line)
                elif log_time < '19:30:00':
                    time_190.append(line)
                elif log_time < '20:00:00':
                    time_195.append(line)
                elif log_time < '20:30:00':
                    time_200.append(line)
                elif log_time < '21:00:00':
                    time_205.append(line)
                elif log_time < '21:30:00':
                    time_210.append(line)
                elif log_time < '22:00:00':
                    time_215.append(line)
                elif log_time < '22:30:00':
                    time_220.append(line)
                elif log_time < '23:00:00':
                    time_225.append(line)
                elif log_time < '23:30:00':
                    time_230.append(line)
                else:
                    time_235.append(line)

        time_000_pv = len(time_000)
        _000_uv = set()
        time_000_codesum = 0
        for _000 in time_000:
            _000_uv.add(_000.split(' ')[0])
            if _000.split(' ')[9].isdigit():
                time_000_codesum += int(_000.split(' ')[9])
            else:
                time_000_codesum += 0
        time_000_uv = len(_000_uv)
        time_000_codesum = round(time_000_codesum / 1048576, 2)

        time_005_pv = len(time_005)
        _005_uv = set()
        time_005_codesum = 0
        for _005 in time_005:
            _005_uv.add(_005.split(' ')[0])
            if _005.split(' ')[9].isdigit():
                time_005_codesum += int(_005.split(' ')[9])
            else:
                time_005_codesum += 0
        time_005_uv = len(_005_uv)
        time_005_codesum = round(time_005_codesum / 1048576, 2)

        time_010_pv = len(time_010)
        _010_uv = set()
        time_010_codesum = 0
        for _010 in time_010:
            _010_uv.add(_010.split(' ')[0])
            if _010.split(' ')[9].isdigit():
                time_010_codesum += int(_010.split(' ')[9])
            else:
                time_010_codesum += 0
        time_010_uv = len(_010_uv)
        time_010_codesum = round(time_010_codesum / 1048576, 2)

        time_015_pv = len(time_015)
        _015_uv = set()
        time_015_codesum = 0
        for _015 in time_015:
            _015_uv.add(_015.split(' ')[0])
            if _015.split(' ')[9].isdigit():
                time_015_codesum += int(_015.split(' ')[9])
            else:
                time_015_codesum += 0
        time_015_uv = len(_015_uv)
        time_015_codesum = round(time_015_codesum / 1048576, 2)

        time_020_pv = len(time_020)
        _020_uv = set()
        time_020_codesum = 0
        for _020 in time_020:
            _020_uv.add(_020.split(' ')[0])
            if _020.split(' ')[9].isdigit():
                time_020_codesum += int(_020.split(' ')[9])
            else:
                time_020_codesum += 0
        time_020_uv = len(_020_uv)
        time_020_codesum = round(time_020_codesum / 1048576, 2)

        time_025_pv = len(time_025)
        _025_uv = set()
        time_025_codesum = 0
        for _025 in time_025:
            _025_uv.add(_025.split(' ')[0])
            if _025.split(' ')[9].isdigit():
                time_025_codesum += int(_025.split(' ')[9])
            else:
                time_025_codesum += 0
        time_025_uv = len(_025_uv)
        time_025_codesum = round(time_025_codesum / 1048576, 2)

        time_030_pv = len(time_030)
        _030_uv = set()
        time_030_codesum = 0
        for _030 in time_030:
            _030_uv.add(_030.split(' ')[0])
            if _030.split(' ')[9].isdigit():
                time_030_codesum += int(_030.split(' ')[9])
            else:
                time_030_codesum += 0
        time_030_uv = len(_030_uv)
        time_030_codesum = round(time_030_codesum / 1048576, 2)

        time_035_pv = len(time_035)
        _035_uv = set()
        time_035_codesum = 0
        for _035 in time_035:
            _035_uv.add(_035.split(' ')[0])
            if _035.split(' ')[9].isdigit():
                time_035_codesum += int(_035.split(' ')[9])
            else:
                time_035_codesum += 0
        time_035_uv = len(_035_uv)
        time_035_codesum = round(time_035_codesum / 1048576, 2)

        time_040_pv = len(time_040)
        _040_uv = set()
        time_040_codesum = 0
        for _040 in time_040:
            _040_uv.add(_040.split(' ')[0])
            if _040.split(' ')[9].isdigit():
                time_040_codesum += int(_040.split(' ')[9])
            else:
                time_040_codesum += 0
        time_040_uv = len(_040_uv)
        time_040_codesum = round(time_040_codesum / 1048576, 2)

        time_045_pv = len(time_045)
        _045_uv = set()
        time_045_codesum = 0
        for _045 in time_045:
            _045_uv.add(_045.split(' ')[0])
            if _045.split(' ')[9].isdigit():
                time_045_codesum += int(_045.split(' ')[9])
            else:
                time_045_codesum += 0
        time_045_uv = len(_045_uv)
        time_045_codesum = round(time_045_codesum / 1048576, 2)

        time_050_pv = len(time_050)
        _050_uv = set()
        time_050_codesum = 0
        for _050 in time_050:
            _050_uv.add(_050.split(' ')[0])
            if _050.split(' ')[9].isdigit():
                time_050_codesum += int(_050.split(' ')[9])
            else:
                time_050_codesum += 0
        time_050_uv = len(_050_uv)
        time_050_codesum = round(time_050_codesum / 1048576, 2)

        time_055_pv = len(time_055)
        _055_uv = set()
        time_055_codesum = 0
        for _055 in time_055:
            _055_uv.add(_055.split(' ')[0])
            if _055.split(' ')[9].isdigit():
                time_055_codesum += int(_055.split(' ')[9])
            else:
                time_055_codesum += 0
        time_055_uv = len(_055_uv)
        time_055_codesum = round(time_055_codesum / 1048576, 2)

        time_060_pv = len(time_060)
        _060_uv = set()
        time_060_codesum = 0
        for _060 in time_060:
            _060_uv.add(_060.split(' ')[0])
            if _060.split(' ')[9].isdigit():
                time_060_codesum += int(_060.split(' ')[9])
            else:
                time_060_codesum += 0
        time_060_uv = len(_060_uv)
        time_060_codesum = round(time_060_codesum / 1048576, 2)

        time_065_pv = len(time_065)
        _065_uv = set()
        time_065_codesum = 0
        for _065 in time_065:
            _065_uv.add(_065.split(' ')[0])
            if _065.split(' ')[9].isdigit():
                time_065_codesum += int(_065.split(' ')[9])
            else:
                time_065_codesum += 0
        time_065_uv = len(_065_uv)
        time_065_codesum = round(time_065_codesum / 1048576, 2)

        time_070_pv = len(time_070)
        _070_uv = set()
        time_070_codesum = 0
        for _070 in time_070:
            _070_uv.add(_070.split(' ')[0])
            if _070.split(' ')[9].isdigit():
                time_070_codesum += int(_070.split(' ')[9])
            else:
                time_070_codesum += 0
        time_070_uv = len(_070_uv)
        time_070_codesum = round(time_070_codesum / 1048576, 2)

        time_075_pv = len(time_075)
        _075_uv = set()
        time_075_codesum = 0
        for _075 in time_075:
            _075_uv.add(_075.split(' ')[0])
            if _075.split(' ')[9].isdigit():
                time_075_codesum += int(_075.split(' ')[9])
            else:
                time_075_codesum += 0
        time_075_uv = len(_075_uv)
        time_075_codesum = round(time_075_codesum / 1048576, 2)

        time_080_pv = len(time_080)
        _080_uv = set()
        time_080_codesum = 0
        for _080 in time_080:
            _080_uv.add(_080.split(' ')[0])
            if _080.split(' ')[9].isdigit():
                time_080_codesum += int(_080.split(' ')[9])
            else:
                time_080_codesum += 0
        time_080_uv = len(_080_uv)
        time_080_codesum = round(time_080_codesum / 1048576, 2)

        time_085_pv = len(time_085)
        _085_uv = set()
        time_085_codesum = 0
        for _085 in time_085:
            _085_uv.add(_085.split(' ')[0])
            if _085.split(' ')[9].isdigit():
                time_085_codesum += int(_085.split(' ')[9])
            else:
                time_085_codesum += 0
        time_085_uv = len(_085_uv)
        time_085_codesum = round(time_085_codesum / 1048576, 2)

        time_090_pv = len(time_090)
        _090_uv = set()
        time_090_codesum = 0
        for _090 in time_090:
            _090_uv.add(_090.split(' ')[0])
            if _090.split(' ')[9].isdigit():
                time_090_codesum += int(_090.split(' ')[9])
            else:
                time_090_codesum += 0
        time_090_uv = len(_090_uv)
        time_090_codesum = round(time_090_codesum / 1048576, 2)

        time_095_pv = len(time_095)
        _095_uv = set()
        time_095_codesum = 0
        for _095 in time_095:
            _095_uv.add(_095.split(' ')[0])
            if _095.split(' ')[9].isdigit():
                time_095_codesum += int(_095.split(' ')[9])
            else:
                time_095_codesum += 0
        time_095_uv = len(_095_uv)
        time_095_codesum = round(time_095_codesum / 1048576, 2)

        time_100_pv = len(time_100)
        _100_uv = set()
        time_100_codesum = 0
        for _100 in time_100:
            _100_uv.add(_100.split(' ')[0])
            if _100.split(' ')[9].isdigit():
                time_100_codesum += int(_100.split(' ')[9])
            else:
                time_100_codesum += 0
        time_100_uv = len(_100_uv)
        time_100_codesum = round(time_100_codesum / 1048576, 2)

        time_105_pv = len(time_105)
        _105_uv = set()
        time_105_codesum = 0
        for _105 in time_105:
            _105_uv.add(_105.split(' ')[0])
            if _105.split(' ')[9].isdigit():
                time_105_codesum += int(_105.split(' ')[9])
            else:
                time_105_codesum += 0
        time_105_uv = len(_105_uv)
        time_105_codesum = round(time_105_codesum / 1048576, 2)

        time_110_pv = len(time_110)
        _110_uv = set()
        time_110_codesum = 0
        for _110 in time_110:
            _110_uv.add(_110.split(' ')[0])
            if _110.split(' ')[9].isdigit():
                time_110_codesum += int(_110.split(' ')[9])
            else:
                time_110_codesum += 0
        time_110_uv = len(_110_uv)
        time_110_codesum = round(time_110_codesum / 1048576, 2)

        time_115_pv = len(time_115)
        _115_uv = set()
        time_115_codesum = 0
        for _115 in time_115:
            _115_uv.add(_115.split(' ')[0])
            if _115.split(' ')[9].isdigit():
                time_115_codesum += int(_115.split(' ')[9])
            else:
                time_115_codesum += 0
        time_115_uv = len(_115_uv)
        time_115_codesum = round(time_115_codesum / 1048576, 2)

        time_120_pv = len(time_120)
        _120_uv = set()
        time_120_codesum = 0
        for _120 in time_120:
            _120_uv.add(_120.split(' ')[0])
            if _120.split(' ')[9].isdigit():
                time_120_codesum += int(_120.split(' ')[9])
            else:
                time_120_codesum += 0
        time_120_uv = len(_120_uv)
        time_120_codesum = round(time_120_codesum / 1048576, 2)

        time_125_pv = len(time_125)
        _125_uv = set()
        time_125_codesum = 0
        for _125 in time_125:
            _125_uv.add(_125.split(' ')[0])
            if _125.split(' ')[9].isdigit():
                time_125_codesum += int(_125.split(' ')[9])
            else:
                time_125_codesum += 0
        time_125_uv = len(_125_uv)
        time_125_codesum = round(time_125_codesum / 1048576, 2)

        time_130_pv = len(time_130)
        _130_uv = set()
        time_130_codesum = 0
        for _130 in time_130:
            _130_uv.add(_130.split(' ')[0])
            if _130.split(' ')[9].isdigit():
                time_130_codesum += int(_130.split(' ')[9])
            else:
                time_130_codesum += 0
        time_130_uv = len(_130_uv)
        time_130_codesum = round(time_130_codesum / 1048576, 2)

        time_135_pv = len(time_135)
        _135_uv = set()
        time_135_codesum = 0
        for _135 in time_135:
            _135_uv.add(_135.split(' ')[0])
            if _135.split(' ')[9].isdigit():
                time_135_codesum += int(_135.split(' ')[9])
            else:
                time_135_codesum += 0
        time_135_uv = len(_135_uv)
        time_135_codesum = round(time_135_codesum / 1048576, 2)

        time_140_pv = len(time_140)
        _140_uv = set()
        time_140_codesum = 0
        for _140 in time_140:
            _140_uv.add(_140.split(' ')[0])
            if _140.split(' ')[9].isdigit():
                time_140_codesum += int(_140.split(' ')[9])
            else:
                time_140_codesum += 0
        time_140_uv = len(_140_uv)
        time_140_codesum = round(time_140_codesum / 1048576, 2)

        time_145_pv = len(time_145)
        _145_uv = set()
        time_145_codesum = 0
        for _145 in time_145:
            _145_uv.add(_145.split(' ')[0])
            if _145.split(' ')[9].isdigit():
                time_145_codesum += int(_145.split(' ')[9])
            else:
                time_145_codesum += 0
        time_145_uv = len(_145_uv)
        time_145_codesum = round(time_145_codesum / 1048576, 2)

        time_150_pv = len(time_150)
        _150_uv = set()
        time_150_codesum = 0
        for _150 in time_150:
            _150_uv.add(_150.split(' ')[0])
            if _150.split(' ')[9].isdigit():
                time_150_codesum += int(_150.split(' ')[9])
            else:
                time_150_codesum += 0
        time_150_uv = len(_150_uv)
        time_150_codesum = round(time_150_codesum / 1048576, 2)

        time_155_pv = len(time_155)
        _155_uv = set()
        time_155_codesum = 0
        for _155 in time_155:
            _155_uv.add(_155.split(' ')[0])
            if _155.split(' ')[9].isdigit():
                time_155_codesum += int(_155.split(' ')[9])
            else:
                time_155_codesum += 0
        time_155_uv = len(_155_uv)
        time_155_codesum = round(time_155_codesum / 1048576, 2)

        time_160_pv = len(time_160)
        _160_uv = set()
        time_160_codesum = 0
        for _160 in time_160:
            _160_uv.add(_160.split(' ')[0])
            if _160.split(' ')[9].isdigit():
                time_160_codesum += int(_160.split(' ')[9])
            else:
                time_160_codesum += 0
        time_160_uv = len(_160_uv)
        time_160_codesum = round(time_160_codesum / 1048576, 2)

        time_165_pv = len(time_165)
        _165_uv = set()
        time_165_codesum = 0
        for _165 in time_165:
            _165_uv.add(_165.split(' ')[0])
            if _165.split(' ')[9].isdigit():
                time_165_codesum += int(_165.split(' ')[9])
            else:
                time_165_codesum += 0
        time_165_uv = len(_165_uv)
        time_165_codesum = round(time_165_codesum / 1048576, 2)

        time_170_pv = len(time_170)
        _170_uv = set()
        time_170_codesum = 0
        for _170 in time_170:
            _170_uv.add(_170.split(' ')[0])
            if _170.split(' ')[9].isdigit():
                time_170_codesum += int(_170.split(' ')[9])
            else:
                time_170_codesum += 0
        time_170_uv = len(_170_uv)
        time_170_codesum = round(time_170_codesum / 1048576, 2)

        time_175_pv = len(time_175)
        _175_uv = set()
        time_175_codesum = 0
        for _175 in time_175:
            _175_uv.add(_175.split(' ')[0])
            if _175.split(' ')[9].isdigit():
                time_175_codesum += int(_175.split(' ')[9])
            else:
                time_175_codesum += 0
        time_175_uv = len(_175_uv)
        time_175_codesum = round(time_175_codesum / 1048576, 2)

        time_180_pv = len(time_180)
        _180_uv = set()
        time_180_codesum = 0
        for _180 in time_180:
            _180_uv.add(_180.split(' ')[0])
            if _180.split(' ')[9].isdigit():
                time_180_codesum += int(_180.split(' ')[9])
            else:
                time_180_codesum += 0
        time_180_uv = len(_180_uv)
        time_180_codesum = round(time_180_codesum / 1048576, 2)

        time_185_pv = len(time_185)
        _185_uv = set()
        time_185_codesum = 0
        for _185 in time_185:
            _185_uv.add(_185.split(' ')[0])
            if _185.split(' ')[9].isdigit():
                time_185_codesum += int(_185.split(' ')[9])
            else:
                time_185_codesum += 0
        time_185_uv = len(_185_uv)
        time_185_codesum = round(time_185_codesum / 1048576, 2)

        time_190_pv = len(time_190)
        _190_uv = set()
        time_190_codesum = 0
        for _190 in time_190:
            _190_uv.add(_190.split(' ')[0])
            if _190.split(' ')[9].isdigit():
                time_190_codesum += int(_190.split(' ')[9])
            else:
                time_190_codesum += 0
        time_190_uv = len(_190_uv)
        time_190_codesum = round(time_190_codesum / 1048576, 2)

        time_195_pv = len(time_195)
        _195_uv = set()
        time_195_codesum = 0
        for _195 in time_195:
            _195_uv.add(_195.split(' ')[0])
            if _195.split(' ')[9].isdigit():
                time_195_codesum += int(_195.split(' ')[9])
            else:
                time_195_codesum += 0
        time_195_uv = len(_195_uv)
        time_195_codesum = round(time_195_codesum / 1048576, 2)

        time_200_pv = len(time_200)
        _200_uv = set()
        time_200_codesum = 0
        for _200 in time_200:
            _200_uv.add(_200.split(' ')[0])
            if _200.split(' ')[9].isdigit():
                time_200_codesum += int(_200.split(' ')[9])
            else:
                time_200_codesum += 0
        time_200_uv = len(_200_uv)
        time_200_codesum = round(time_200_codesum / 1048576, 2)

        time_205_pv = len(time_205)
        _205_uv = set()
        time_205_codesum = 0
        for _205 in time_205:
            _205_uv.add(_205.split(' ')[0])
            if _205.split(' ')[9].isdigit():
                time_205_codesum += int(_205.split(' ')[9])
            else:
                time_205_codesum += 0
        time_205_uv = len(_205_uv)
        time_205_codesum = round(time_205_codesum / 1048576, 2)

        time_210_pv = len(time_210)
        _210_uv = set()
        time_210_codesum = 0
        for _210 in time_210:
            _210_uv.add(_210.split(' ')[0])
            if _210.split(' ')[9].isdigit():
                time_210_codesum += int(_210.split(' ')[9])
            else:
                time_210_codesum += 0
        time_210_uv = len(_210_uv)
        time_210_codesum = round(time_210_codesum / 1048576, 2)

        time_215_pv = len(time_215)
        _215_uv = set()
        time_215_codesum = 0
        for _215 in time_215:
            _215_uv.add(_215.split(' ')[0])
            if _215.split(' ')[9].isdigit():
                time_215_codesum += int(_215.split(' ')[9])
            else:
                time_215_codesum += 0
        time_215_uv = len(_215_uv)
        time_215_codesum = round(time_215_codesum / 1048576, 2)

        time_220_pv = len(time_220)
        _220_uv = set()
        time_220_codesum = 0
        for _220 in time_220:
            _220_uv.add(_220.split(' ')[0])
            if _220.split(' ')[9].isdigit():
                time_220_codesum += int(_220.split(' ')[9])
            else:
                time_220_codesum += 0
        time_220_uv = len(_220_uv)
        time_220_codesum = round(time_220_codesum / 1048576, 2)

        time_225_pv = len(time_225)
        _225_uv = set()
        time_225_codesum = 0
        for _225 in time_225:
            _225_uv.add(_225.split(' ')[0])
            if _225.split(' ')[9].isdigit():
                time_225_codesum += int(_225.split(' ')[9])
            else:
                time_225_codesum += 0
        time_225_uv = len(_225_uv)
        time_225_codesum = round(time_225_codesum / 1048576, 2)

        time_230_pv = len(time_230)
        _230_uv = set()
        time_230_codesum = 0
        for _230 in time_230:
            _230_uv.add(_230.split(' ')[0])
            if _230.split(' ')[9].isdigit():
                time_230_codesum += int(_230.split(' ')[9])
            else:
                time_230_codesum += 0
        time_230_uv = len(_230_uv)
        time_230_codesum = round(time_230_codesum / 1048576, 2)

        time_235_pv = len(time_235)
        _235_uv = set()
        time_235_codesum = 0
        for _235 in time_235:
            _235_uv.add(_235.split(' ')[0])
            if _235.split(' ')[9].isdigit():
                time_235_codesum += int(_235.split(' ')[9])
            else:
                time_235_codesum += 0
        time_235_uv = len(_235_uv)
        time_235_codesum = round(time_235_codesum / 1048576, 2)

        temp = {'time_day': ['00:00:00', '00:30:00', '01:00:00', '01:30:00', '02:00:00', '02:30:00',
                             '03:00:00', '03:30:00', '04:00:00', '04:30:00', '05:00:00', '05:30:00',
                             '06:00:00', '06:30:00', '07:00:00', '07:30:00', '08:00:00', '08:30:00',
                             '09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00',
                             '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00',
                             '15:00:00', '15:30:00', '16:00:00', '16:30:00', '17:00:00', '17:30:00',
                             '18:00:00', '18:30:00', '19:00:00', '19:30:00', '20:00:00', '20:30:00',
                             '21:00:00', '21:30:00', '22:00:00', '22:30:00', '23:00:00', '23:30:00'],
                'pv': [time_000_pv, time_005_pv, time_010_pv, time_015_pv, time_020_pv, time_025_pv,
                       time_030_pv, time_035_pv, time_040_pv, time_045_pv, time_050_pv, time_055_pv,
                       time_060_pv, time_065_pv, time_070_pv, time_075_pv, time_080_pv, time_085_pv,
                       time_090_pv, time_095_pv, time_100_pv, time_105_pv, time_110_pv, time_115_pv,
                       time_120_pv, time_125_pv, time_130_pv, time_135_pv, time_140_pv, time_145_pv,
                       time_150_pv, time_155_pv, time_160_pv, time_165_pv, time_170_pv, time_175_pv,
                       time_180_pv, time_185_pv, time_190_pv, time_195_pv, time_200_pv, time_205_pv,
                       time_210_pv, time_215_pv, time_220_pv, time_225_pv, time_230_pv, time_235_pv],
                'uv': [time_000_uv, time_005_uv, time_010_uv, time_015_uv, time_020_uv, time_025_uv,
                       time_030_uv, time_035_uv, time_040_uv, time_045_uv, time_050_uv, time_055_uv,
                       time_060_uv, time_065_uv, time_070_uv, time_075_uv, time_080_uv, time_085_uv,
                       time_090_uv, time_095_uv, time_100_uv, time_105_uv, time_110_uv, time_115_uv,
                       time_120_uv, time_125_uv, time_130_uv, time_135_uv, time_140_uv, time_145_uv,
                       time_150_uv, time_155_uv, time_160_uv, time_165_uv, time_170_uv, time_175_uv,
                       time_180_uv, time_185_uv, time_190_uv, time_195_uv, time_200_uv, time_205_uv,
                       time_210_uv, time_215_uv, time_220_uv, time_225_uv, time_230_uv, time_235_uv],
                'outflux': [time_000_codesum, time_005_codesum, time_010_codesum, time_015_codesum,
                            time_020_codesum, time_025_codesum, time_030_codesum, time_035_codesum,
                            time_040_codesum, time_045_codesum, time_050_codesum, time_055_codesum,
                            time_060_codesum, time_065_codesum, time_070_codesum, time_075_codesum,
                            time_080_codesum, time_085_codesum, time_090_codesum, time_095_codesum,
                            time_100_codesum, time_105_codesum, time_110_codesum, time_115_codesum,
                            time_120_codesum, time_125_codesum, time_130_codesum, time_135_codesum,
                            time_140_codesum, time_145_codesum, time_150_codesum, time_155_codesum,
                            time_160_codesum, time_165_codesum, time_170_codesum, time_175_codesum,
                            time_180_codesum, time_185_codesum, time_190_codesum, time_195_codesum,
                            time_200_codesum, time_205_codesum, time_210_codesum, time_215_codesum,
                            time_220_codesum, time_225_codesum, time_230_codesum, time_235_codesum],
                'influx': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'code': 0, 'msg': ""}
        return temp
